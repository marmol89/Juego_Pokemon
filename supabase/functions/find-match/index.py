"""
Edge Function: find-match
Triggered via POST after INSERT on matchmaking_queue.
Finds a matching candidate and creates a room if found.
"""
import os
import sys
from supabase import create_client, Client
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE
import json


def get_db_connection():
    """Get PostgreSQL connection from environment."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return connect(database_url)
    
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    
    if all([host, port, dbname, user, password]):
        return connect(
            host=host, port=port, dbname=dbname, 
            user=user, password=password
        )
    
    raise RuntimeError("No database connection configuration found")


def find_match_candidates(conn, rating: int, rating_diff_max: int):
    """Find matching candidates using the PostgreSQL function."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT user_id, rating, entered_at, id
        FROM find_match_candidates(%s, %s)
        FOR UPDATE
        """,
        (rating, rating_diff_max)
    )
    return cursor.fetchone()


def handler(req: dict) -> dict:
    """
    Main handler for the Edge Function.
    
    Expected payload:
    {
        "new_entry_id": int,
        "user_id": str,
        "rating": int (optional, will query if not provided)
    }
    """
    try:
        # Parse payload
        body = req.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)
        
        new_entry_id = body.get("new_entry_id")
        user_id = body.get("user_id")
        rating = body.get("rating")
        rating_diff_max = body.get("rating_diff_max", 50)
        
        if not new_entry_id or not user_id:
            return {"status": "error", "message": "Missing required fields"}
        
        # Connect to database
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_SERIALIZABLE)
        
        try:
            cursor = conn.cursor()
            
            # Step 1: Lock and verify the new entry
            cursor.execute(
                """
                SELECT id, status, rating, user_id FROM matchmaking_queue
                WHERE id = %s AND status = 'waiting'
                FOR UPDATE
                """,
                (new_entry_id,)
            )
            entry = cursor.fetchone()
            if entry is None:
                conn.rollback()
                return {"status": "skipped", "reason": "entry_not_found"}
            
            entry_rating = entry[2]
            
            # Step 2: Find the best candidate
            candidate = find_match_candidates(conn, entry_rating, rating_diff_max)
            
            if candidate is None:
                conn.commit()
                return {"status": "no_match", "entry_id": new_entry_id}
            
            matched_user_id = candidate[0]
            candidate_id = candidate[3]
            
            # Step 3: Create room
            cursor.execute(
                """
                INSERT INTO rooms (user_id, enemigo_id, nombre, estado)
                VALUES (%s, %s, %s, 2)
                RETURNING id
                """,
                (user_id, matched_user_id, f"Match_{new_entry_id}_{candidate_id}")
            )
            room_id = cursor.fetchone()[0]
            
            # Step 4: Update candidate entry to 'matched'
            cursor.execute(
                """
                UPDATE matchmaking_queue
                SET status = 'matched', room_id = %s
                WHERE id = %s
                """,
                (room_id, candidate_id)
            )
            
            # Step 5: Update new entry to 'matched'
            cursor.execute(
                """
                UPDATE matchmaking_queue
                SET status = 'matched', room_id = %s
                WHERE id = %s
                """,
                (room_id, new_entry_id)
            )
            
            conn.commit()
            
            # Step 6: Broadcast match_found via Realtime
            broadcast_match_found(matched_user_id, user_id, room_id, conn)
            
            return {
                "status": "matched",
                "room_id": str(room_id),
                "opponent_id": matched_user_id
            }
            
        except Exception as e:
            conn.rollback()
            print(f"[find-match] Error: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            conn.close()
            
    except Exception as e:
        print(f"[find-match] Handler error: {e}")
        return {"status": "error", "message": str(e)}


def broadcast_match_found(user_a: str, user_b: str, room_id, conn):
    """Broadcast match_found event to both users via Supabase Realtime."""
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("[find-match] Supabase credentials not found for realtime broadcast")
            return
        
        client: Client = create_client(supabase_url, supabase_key)
        room_id_str = str(room_id)
        
        # Broadcast to user A
        channel_a = client.channel(f"matchmaking:{user_a}")
        channel_a.on_event("broadcast", lambda e: None)
        channel_a.subscribe()
        channel_a.send_broadcast(
            event="match_found",
            payload={"room_id": room_id_str}
        )
        
        # Broadcast to user B  
        channel_b = client.channel(f"matchmaking:{user_b}")
        channel_b.on_event("broadcast", lambda e: None)
        channel_b.subscribe()
        channel_b.send_broadcast(
            event="match_found",
            payload={"room_id": room_id_str}
        )
        
    except Exception as e:
        print(f"[find-match] Realtime broadcast error: {e}")


# Supabase Edge Function entry point
def main(req: dict):
    return handler(req)


if __name__ == "__main__":
    test_req = {
        "body": {
            "new_entry_id": 1,
            "user_id": "test-user-uuid",
            "rating": 1000
        }
    }
    print(handler(test_req))
