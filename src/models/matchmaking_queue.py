from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional


@dataclass
class MatchmakingQueue:
    """
    Represents an entry in the matchmaking queue.

    Attributes:
        id: Primary key
        user_id: UUID of the user in queue
        rating: User's current rating (puntos)
        rating_diff_max: Maximum rating difference allowed for matching
        status: One of 'waiting', 'matched', 'timeout', 'abandoned'
        room_id: UUID of matched room (only if status='matched')
        entered_at: Timestamp when user entered queue
        updated_at: Timestamp of last update
    """
    id: int
    user_id: str
    rating: int
    rating_diff_max: int
    status: Literal['waiting', 'matched', 'timeout', 'abandoned']
    room_id: Optional[str]
    entered_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: dict) -> 'MatchmakingQueue':
        """Create instance from database row dict."""
        return cls(
            id=row['id'],
            user_id=row['user_id'],
            rating=row['rating'],
            rating_diff_max=row.get('rating_diff_max', 50),
            status=row['status'],
            room_id=row.get('room_id'),
            entered_at=row['entered_at'],
            updated_at=row['updated_at']
        )

    def is_waiting(self) -> bool:
        """Returns True if entry is still in waiting status."""
        return self.status == 'waiting'

    def is_matched(self) -> bool:
        """Returns True if entry has been matched."""
        return self.status == 'matched'

    def is_expired(self) -> bool:
        """Returns True if entry has timed out."""
        return self.status == 'timeout'
