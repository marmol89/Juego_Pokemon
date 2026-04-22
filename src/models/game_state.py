import threading
from typing import List, Optional, Any

class GameState:
    """
    Singleton GameState to manage global game state across the application.
    Thread-safe implementation using double-checked locking.
    """
    _instance: Optional['GameState'] = None
    _lock = threading.Lock()
    
    def __init__(self):
        self._equipoA: List[Any] = []
        self._equipoE: List[Any] = []
        self._pokemons: List[Any] = []
        self._current_user: Any = None
    
    @classmethod
    def get_instance(cls) -> 'GameState':
        """
        Returns the singleton instance of GameState.
        Uses double-checked locking for thread safety.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    @property
    def equipoA(self) -> List[Any]:
        return self._equipoA
    
    @equipoA.setter
    def equipoA(self, value: List[Any]):
        self._equipoA = value
    
    @property
    def equipoE(self) -> List[Any]:
        return self._equipoE
    
    @equipoE.setter
    def equipoE(self, value: List[Any]):
        self._equipoE = value
    
    @property
    def pokemons(self) -> List[Any]:
        return self._pokemons
    
    @pokemons.setter
    def pokemons(self, value: List[Any]):
        self._pokemons = value
    
    @property
    def current_user(self) -> Any:
        return self._current_user
    
    @current_user.setter
    def current_user(self, value: Any):
        self._current_user = value
    
    def set_team(self, side: str, team: List[Any]) -> None:
        """
        Sets the team for the specified side.
        
        Args:
            side: 'A' for user team, 'E' for enemy team
            team: The team list to set
        """
        if side.upper() == 'A':
            self._equipoA = team
        elif side.upper() == 'E':
            self._equipoE = team
        else:
            raise ValueError("Side must be 'A' or 'E'")
    
    def reset(self) -> None:
        """
        Resets all game state to initial values.
        """
        self._equipoA = []
        self._equipoE = []
        self._pokemons = []
        self._current_user = None
