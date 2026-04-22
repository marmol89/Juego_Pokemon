import os
import time
from typing import Dict, Callable, Any, Optional

class BattleRealtime:
    """
    Manages Supabase Realtime subscriptions for battle events.
    Provides fallback to polling if Realtime fails.
    """
    
    def __init__(self):
        self.channel = None
        self.battle_id = None
        self.handlers = {}
        self.realtime_enabled = os.getenv('REALTIME_BATTLE_ENABLED', 'true').lower() == 'true'
    
    def subscribe(self, battle_id: int, handlers: Dict[str, Callable]) -> None:
        """
        Subscribe to Supabase channel for battle events.
        
        Args:
            battle_id: The battle room ID
            handlers: Dict with keys 'on_player_action', 'on_opponent_action', 'on_battle_end'
        """
        self.battle_id = battle_id
        self.handlers = handlers
        
        if not self.realtime_enabled:
            return
        
        try:
            from supabase import create_client, Client
            from src.config import SUPABASE_URL, SUPABASE_KEY
            
            if not SUPABASE_URL or not SUPABASE_KEY:
                return
            
            client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            
            self.channel = client.channel(f'battle_{battle_id}')
            
            self.channel.on_event("broadcast", handlers.get('on_player_action', lambda e: None))
            self.channel.on_event("broadcast", handlers.get('on_opponent_action', lambda e: None))
            self.channel.on_event("broadcast", handlers.get('on_battle_end', lambda e: None))
            
            self.channel.subscribe()
        except Exception as e:
            # Fallback to None - polling will be used
            self.channel = None
    
    def unsubscribe(self) -> None:
        """
        Cleanup subscription to Supabase channel.
        """
        if self.channel:
            try:
                self.channel.unsubscribe()
            except:
                pass
            self.channel = None
        self.battle_id = None
        self.handlers = {}
    
    def on_player_action(self, event: Any) -> None:
        """Handler for player action broadcast events."""
        if self.handlers.get('on_player_action'):
            self.handlers['on_player_action'](event)
    
    def on_opponent_action(self, event: Any) -> None:
        """Handler for opponent action broadcast events."""
        if self.handlers.get('on_opponent_action'):
            self.handlers['on_opponent_action'](event)
    
    def on_battle_end(self, event: Any) -> None:
        """Handler for battle end broadcast events."""
        if self.handlers.get('on_battle_end'):
            self.handlers['on_battle_end'](event)
    
    def is_connected(self) -> bool:
        """Returns True if Realtime channel is connected."""
        return self.channel is not None
