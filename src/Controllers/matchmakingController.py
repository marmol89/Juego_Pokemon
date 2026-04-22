"""
MatchmakingController: Handles matchmaking queue operations.
Orchestrates the matchmaking DAO and realtime notifications.
"""
from typing import Optional, Tuple
from src.database.matchmaking import MatchmakingDAO
from src.database.users import users
from src.database.rooms import rooms
from src.database.battles import battles
from src.utils.matchmaking_realtime import MatchmakingRealtime


class MatchmakingController:
    """
    Controller for matchmaking queue operations.
    Coordinates between the DAO, database models, and realtime notifications.
    """
    
    def __init__(self):
        self.dao = MatchmakingDAO()
        self.users_db = users()
        self.rooms_db = rooms()
        self.battles_db = battles()
        self.realtime = MatchmakingRealtime()
    
    def join_queue(self, user) -> Tuple[bool, str, Optional[int]]:
        """
        Attempt to join the matchmaking queue.
        
        Args:
            user: Logged-in user object (must have id and puntos attributes)
            
        Returns:
            Tuple of (success: bool, message: str, entry_id: Optional[int])
        """
        from src.database.teams import teams
        
        # Verify user has a team
        user_teams = teams()
        # Note: teams table needs room_id - for matchmaking, we just check if user has any team entries
        # This is a simplified check - in a real app, you'd have a user_teams table
        team_check = self._user_has_team(user.id)
        if not team_check:
            return (False, "Primero necesitas un equipo", None)
        
        # Check if user already in queue
        existing = self.dao.get_status(user.id)
        if existing is not None:
            return (False, "Ya estás en la cola de búsqueda", None)
        
        # Join the queue with user's rating
        # First, clean up any abandoned entries from disconnected users
        self.dao.cleanup_abandoned()

        rating = getattr(user, 'puntos', 0)
        entry_id = self.dao.join_queue(str(user.id), rating)
        
        if entry_id is None:
            return (False, "No se pudo unir a la cola", None)
        
        # Subscribe to realtime events
        self.realtime.subscribe(str(user.id), {
            'on_match_found': lambda room_id: self._on_match_found(user.id, room_id),
            'on_timeout': lambda: self._on_timeout(user.id),
            'on_cancelled': lambda: self._on_cancelled(user.id)
        })
        
        return (True, "Buscando partida...", entry_id)
    
    def leave_queue(self, user) -> bool:
        """
        Remove the user from the matchmaking queue.
        
        Args:
            user: Logged-in user object
            
        Returns:
            True if successfully left queue, False otherwise
        """
        # Unsubscribe from realtime
        self.realtime.unsubscribe(str(user.id))
        
        # Remove from queue
        return self.dao.leave_queue(str(user.id))

    def try_match(self, entry_id: int, user_id: str, rating: int, rating_diff_max: int = 50) -> Optional[int]:
        """
        Attempt to find a match for the given queue entry.
        Called periodically from the polling loop in searchMatch.

        Args:
            entry_id: The queue entry ID
            user_id: The user ID
            rating: The user's rating
            rating_diff_max: Maximum rating difference (default 50)

        Returns:
            Room ID if match found, None otherwise
        """
        return self.dao.find_match(entry_id, user_id, rating, rating_diff_max)

    def get_status(self, user) -> Optional[object]:
        """
        Get the current matchmaking status for a user.
        
        Args:
            user: Logged-in user object
            
        Returns:
            MatchmakingQueue entry if exists, None otherwise
        """
        return self.dao.get_status(str(user.id))
    
    def is_in_queue(self, user) -> bool:
        """Check if user is currently in the matchmaking queue."""
        status = self.get_status(user)
        return status is not None and status.is_waiting()
    
    def _user_has_team(self, user_id: str) -> bool:
        """
        Check if user has at least one Pokemon on their team.
        This is a simplified check - queries for any team entries for the user.
        """
        from src.database.db import db
        try:
            dbp = db().get_connection()
            if not dbp:
                return False
            # Check teams table - room_id and user_id should exist
            data = dbp.table("teams").select("id").eq("user_id", user_id).execute()
            return len(data.data) > 0
        except Exception as e:
            print(f"[MatchmakingController] _user_has_team error: {e}")
            return False
    
    def _on_match_found(self, user_id: str, room_id: str) -> None:
        """
        Callback when match_found event is received via Realtime.
        Transition the user into the room.
        """
        try:
            # The room was already created by the Edge Function
            # We need to start the room waiting flow
            from src.Controllers.roomController import roomController
            from src.models.room import room
            
            room_obj = self.rooms_db.getRoom(room_id)
            if room_obj:
                # Transition room to waiting/combat state
                room_obj.estado = 2
                self.rooms_db.updateRoom(room_obj)
                # Create battle record
                self.battles_db.createBattle(room_id)
        except Exception as e:
            print(f"[MatchmakingController] _on_match_found error: {e}")
    
    def _on_timeout(self, user_id: str) -> None:
        """
        Callback when timeout event is received via Realtime.
        """
        # The entry is already cleaned up by the timeout Edge Function
        # Just need to notify UI if needed
        pass
    
    def _on_cancelled(self, user_id: str) -> None:
        """
        Callback when cancelled event is received via Realtime.
        """
        pass
