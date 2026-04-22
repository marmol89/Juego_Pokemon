from typing import Optional, Tuple
import psycopg2
from src.database.db import db
from src.models.matchmaking_queue import MatchmakingQueue


class MatchmakingDAO:
    """
    Data Access Object for matchmaking_queue table.
    Handles all database operations for the matchmaking system.
    """

    def __init__(self):
        self.db_instance = db()

    def _get_connection(self):
        """Get PostgreSQL connection using db's connection string builder."""
        conn_str = self.db_instance._build_pg_connection_string()
        return psycopg2.connect(conn_str)

    def join_queue(self, user_id: str, rating: int, rating_diff_max: int = 50) -> Optional[int]:
        """
        Insert a new entry into the matchmaking queue.

        Args:
            user_id: UUID of the user joining queue
            rating: User's current rating (puntos)
            rating_diff_max: Maximum rating difference allowed (default 50)

        Returns:
            Entry ID if successful, None if user already in queue or error
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            # Check if user is already in queue with 'waiting' status
            cursor.execute(
                "SELECT id FROM matchmaking_queue WHERE user_id = %s AND status = 'waiting'",
                (user_id,)
            )
            if cursor.fetchone() is not None:
                return None  # Already in queue

            # Insert new entry
            cursor.execute(
                """
                INSERT INTO matchmaking_queue (user_id, rating, rating_diff_max, status)
                VALUES (%s, %s, %s, 'waiting')
                RETURNING id
                """,
                (user_id, rating, rating_diff_max)
            )
            entry_id = cursor.fetchone()[0]
            conn.commit()
            return entry_id

        except Exception as e:
            conn.rollback()
            print(f"[MatchmakingDAO] join_queue error: {e}")
            return None
        finally:
            conn.close()

    def leave_queue(self, user_id: str) -> bool:
        """
        Remove a user from the matchmaking queue.

        Args:
            user_id: UUID of the user leaving queue

        Returns:
            True if entry existed and was deleted, False otherwise
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM matchmaking_queue WHERE user_id = %s AND status = 'waiting'",
                (user_id,)
            )
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted

        except Exception as e:
            conn.rollback()
            print(f"[MatchmakingDAO] leave_queue error: {e}")
            return False
        finally:
            conn.close()

    def get_status(self, user_id: str) -> Optional[MatchmakingQueue]:
        """
        Get the current queue entry for a user.

        Args:
            user_id: UUID of the user

        Returns:
            MatchmakingQueue instance if entry exists, None otherwise
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, user_id, rating, rating_diff_max, status, room_id, entered_at, updated_at
                FROM matchmaking_queue
                WHERE user_id = %s AND status = 'waiting'
                """,
                (user_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return None

            return MatchmakingQueue(
                id=row[0],
                user_id=row[1],
                rating=row[2],
                rating_diff_max=row[3],
                status=row[4],
                room_id=row[5],
                entered_at=row[6],
                updated_at=row[7]
            )

        except Exception as e:
            print(f"[MatchmakingDAO] get_status error: {e}")
            return None
        finally:
            conn.close()

    def find_match(self, entry_id: int, user_id: str, rating: int, rating_diff_max: int) -> Optional[Tuple[str, str]]:
        """
        Find a match for the given entry using SERIALIZABLE transaction.
        This is the core matching logic - uses SELECT FOR UPDATE to prevent race conditions.

        Args:
            entry_id: The new entry's ID
            user_id: The new entry's user_id
            rating: The new entry's rating
            rating_diff_max: Maximum rating difference allowed

        Returns:
            Tuple of (matched_user_id, room_id) if match found, None otherwise
        """
        conn = self._get_connection()
        try:
            # Set isolation level to SERIALIZABLE to prevent race conditions
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
            cursor = conn.cursor()

            # Step 1: Lock the new entry to prevent double-matching
            cursor.execute(
                """
                SELECT id, status FROM matchmaking_queue
                WHERE id = %s AND status = 'waiting'
                FOR UPDATE
                """,
                (entry_id,)
            )
            entry = cursor.fetchone()
            if entry is None:
                conn.rollback()
                return None  # Entry already matched or doesn't exist

            # Step 2: Find the best candidate
            cursor.execute(
                """
                SELECT user_id, rating, entered_at, id
                FROM find_match_candidates(%s, %s)
                FOR UPDATE
                """,
                (rating, rating_diff_max)
            )
            candidate = cursor.fetchone()

            if candidate is None:
                conn.commit()
                return None  # No candidates available

            matched_user_id = candidate[0]
            candidate_id = candidate[3]

            # Step 3: Create a new room for the match
            cursor.execute(
                """
                INSERT INTO rooms (user_id, enemigo_id, nombre, estado)
                VALUES (%s, %s, %s, 2)
                RETURNING id
                """,
                (user_id, matched_user_id, f"Match_{entry_id}_{candidate_id}")
            )
            room_id = cursor.fetchone()[0]

            # Step 4: Update candidate entry to 'matched' with room_id
            cursor.execute(
                """
                UPDATE matchmaking_queue
                SET status = 'matched', room_id = %s
                WHERE id = %s
                """,
                (room_id, candidate_id)
            )

            # Step 5: Update new entry to 'matched' with room_id
            cursor.execute(
                """
                UPDATE matchmaking_queue
                SET status = 'matched', room_id = %s
                WHERE id = %s
                """,
                (room_id, entry_id)
            )

            conn.commit()
            return (matched_user_id, str(room_id))

        except psycopg2.extensions.TransactionRollbackError as e:
            # Serialization conflict - another transaction matched the same candidate
            # This is expected behavior - next trigger will retry
            conn.rollback()
            print(f"[MatchmakingDAO] find_match serialization conflict: {e}")
            return None
        except Exception as e:
            conn.rollback()
            print(f"[MatchmakingDAO] find_match error: {e}")
            return None
        finally:
            conn.close()

    def mark_matched(self, user_id: str, room_id: str) -> bool:
        """
        Update entry status to 'matched' and set room_id.

        Args:
            user_id: UUID of the user
            room_id: UUID of the matched room

        Returns:
            True if update succeeded, False otherwise
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE matchmaking_queue
                SET status = 'matched', room_id = %s
                WHERE user_id = %s AND status = 'waiting'
                """,
                (room_id, user_id)
            )
            success = cursor.rowcount > 0
            conn.commit()
            return success

        except Exception as e:
            conn.rollback()
            print(f"[MatchmakingDAO] mark_matched error: {e}")
            return False
        finally:
            conn.close()

    def mark_timeout(self, user_id: str) -> bool:
        """
        Update entry status to 'timeout'.

        Args:
            user_id: UUID of the user

        Returns:
            True if update succeeded, False otherwise
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE matchmaking_queue
                SET status = 'timeout'
                WHERE user_id = %s AND status = 'waiting'
                """,
                (user_id,)
            )
            success = cursor.rowcount > 0
            conn.commit()
            return success

        except Exception as e:
            conn.rollback()
            print(f"[MatchmakingDAO] mark_timeout error: {e}")
            return False
        finally:
            conn.close()

    def mark_abandoned(self, user_id: str) -> bool:
        """
        Update entry status to 'abandoned'.

        Args:
            user_id: UUID of the user

        Returns:
            True if update succeeded, False otherwise
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE matchmaking_queue
                SET status = 'abandoned'
                WHERE user_id = %s AND status = 'waiting'
                """,
                (user_id,)
            )
            success = cursor.rowcount > 0
            conn.commit()
            return success

        except Exception as e:
            conn.rollback()
            print(f"[MatchmakingDAO] mark_abandoned error: {e}")
            return False
        finally:
            conn.close()

    def get_expired_entries(self, timeout_seconds: int = 60) -> list[MatchmakingQueue]:
        """
        Get all entries that have been waiting longer than timeout.

        Args:
            timeout_seconds: Seconds before an entry is considered expired (default 60)

        Returns:
            List of MatchmakingQueue entries that have timed out
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, user_id, rating, rating_diff_max, status, room_id, entered_at, updated_at
                FROM matchmaking_queue
                WHERE status = 'waiting'
                  AND entered_at < now() - interval '%s seconds'
                """,
                (timeout_seconds,)
            )
            rows = cursor.fetchall()
            return [
                MatchmakingQueue(
                    id=row[0],
                    user_id=row[1],
                    rating=row[2],
                    rating_diff_max=row[3],
                    status=row[4],
                    room_id=row[5],
                    entered_at=row[6],
                    updated_at=row[7]
                )
                for row in rows
            ]

        except Exception as e:
            print(f"[MatchmakingDAO] get_expired_entries error: {e}")
            return []
        finally:
            conn.close()

    def delete_entry(self, user_id: str) -> bool:
        """
        Delete a user's queue entry (used after timeout).

        Args:
            user_id: UUID of the user

        Returns:
            True if deletion succeeded, False otherwise
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # Only delete if status is 'waiting' - prevent deleting matched/timeout entries
            cursor.execute(
                "DELETE FROM matchmaking_queue WHERE user_id = %s AND status = 'waiting'",
                (user_id,)
            )
            success = cursor.rowcount > 0
            conn.commit()
            return success

        except Exception as e:
            conn.rollback()
            print(f"[MatchmakingDAO] delete_entry error: {e}")
            return False
        finally:
            conn.close()

    def cleanup_abandoned(self) -> int:
        """
        Clean up orphaned queue entries where the user no longer exists
        or is disconnected.

        Returns:
            Number of entries cleaned up
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # Delete entries where user doesn't exist anymore OR is not connected
            cursor.execute(
                """
                DELETE FROM matchmaking_queue
                WHERE status = 'waiting'
                AND (
                    user_id NOT IN (SELECT id FROM users)
                    OR user_id NOT IN (SELECT user_id FROM auth.sessions WHERE expires_at > now())
                )
                """
            )
            cleaned = cursor.rowcount
            conn.commit()
            return cleaned

        except Exception as e:
            conn.rollback()
            print(f"[MatchmakingDAO] cleanup_abandoned error: {e}")
            return 0
        finally:
            conn.close()
