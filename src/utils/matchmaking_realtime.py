"""
MatchmakingRealtime: Manages Supabase Realtime subscriptions for matchmaking events.
Provides notifications for match_found, timeout, and cancelled events.
"""
import os
from typing import Dict, Callable, Any, Optional

class MatchmakingRealtime:
    """
    Manages Realtime subscriptions for matchmaking events per user.
    
    Events:
        - match_found: { room_id: str }
        - matchmaking_timeout: {}
        - matchmaking_cancelled: {}
    """
    
    def __init__(self):
        self.channels: Dict[str, Any] = {}
        self.handlers: Dict[str, Dict[str, Callable]] = {}
        self.realtime_enabled = os.getenv('REALTIME_MATCHMAKING_ENABLED', 'true').lower() == 'true'
        self._client = None
    
    def _get_client(self):
        """Lazy initialization of Supabase client."""
        if self._client is None:
            try:
                from supabase import create_client
                supabase_url = os.getenv("SUPABASE_URL")
                supabase_key = os.getenv("SUPABASE_KEY")
                if supabase_url and supabase_key:
                    self._client = create_client(supabase_url, supabase_key)
            except Exception as e:
                print(f"[MatchmakingRealtime] Failed to create client: {e}")
                self._client = None
        return self._client
    
    def subscribe(self, user_id: str, handlers: Dict[str, Callable]) -> None:
        """
        Subscribe to matchmaking events for a specific user.
        
        Args:
            user_id: UUID of the user to subscribe to
            handlers: Dict with keys:
                - 'on_match_found': callback(room_id: str)
                - 'on_timeout': callback()
                - 'on_cancelled': callback()
        """
        if not self.realtime_enabled:
            return
        
        client = self._get_client()
        if not client:
            return
        
        try:
            channel_name = f"matchmaking:{user_id}"
            channel = client.channel(channel_name)
            
            # Store handlers
            self.handlers[user_id] = handlers
            
            # Register event handlers
            channel.on_event("broadcast", self._make_handler(user_id, 'on_match_found'))
            channel.on_event("broadcast", self._make_handler(user_id, 'on_timeout'))
            channel.on_event("broadcast", self._make_handler(user_id, 'on_cancelled'))
            
            channel.subscribe()
            self.channels[user_id] = channel
            
        except Exception as e:
            print(f"[MatchmakingRealtime] Subscribe error for {user_id}: {e}")
            self.channels[user_id] = None
    
    def _make_handler(self, user_id: str, event_type: str) -> Callable:
        """Create a handler closure for a specific event type."""
        def handler(event):
            try:
                handlers = self.handlers.get(user_id, {})
                callback = handlers.get(event_type)
                if callback:
                    payload = event.get('payload', {})
                    if event_type == 'on_match_found':
                        callback(payload.get('room_id'))
                    else:
                        callback()
            except Exception as e:
                print(f"[MatchmakingRealtime] Handler error ({event_type}): {e}")
        return handler
    
    def unsubscribe(self, user_id: str) -> None:
        """
        Unsubscribe from matchmaking events for a specific user.
        
        Args:
            user_id: UUID of the user to unsubscribe from
        """
        channel = self.channels.get(user_id)
        if channel:
            try:
                channel.unsubscribe()
            except Exception as e:
                print(f"[MatchmakingRealtime] Unsubscribe error: {e}")
            finally:
                self.channels[user_id] = None
                self.handlers.pop(user_id, None)
    
    def broadcast_match_found(self, user_id: str, room_id: str) -> None:
        """
        Broadcast match_found event to a user.
        (Usually called from Edge Functions, kept here for symmetry)
        """
        self._broadcast(user_id, 'match_found', {'room_id': room_id})
    
    def broadcast_timeout(self, user_id: str) -> None:
        """
        Broadcast timeout event to a user.
        """
        self._broadcast(user_id, 'matchmaking_timeout', {})
    
    def broadcast_cancelled(self, user_id: str) -> None:
        """
        Broadcast cancelled event to a user.
        """
        self._broadcast(user_id, 'matchmaking_cancelled', {})
    
    def _broadcast(self, user_id: str, event: str, payload: Dict) -> None:
        """Internal helper to send a broadcast to a user's channel."""
        channel = self.channels.get(user_id)
        if channel:
            try:
                channel.send_broadcast(event=event, payload=payload)
            except Exception as e:
                print(f"[MatchmakingRealtime] Broadcast error ({event}): {e}")
    
    def is_connected(self, user_id: str) -> bool:
        """Returns True if the user's Realtime channel is connected."""
        channel = self.channels.get(user_id)
        return channel is not None
    
    def cleanup(self) -> None:
        """Unsubscribe all channels and cleanup."""
        for user_id in list(self.channels.keys()):
            self.unsubscribe(user_id)
