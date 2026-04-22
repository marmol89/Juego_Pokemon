import threading
import time
from collections import OrderedDict
from typing import Optional


class PokemonCache:
    def __init__(self, max_size: int = 100, ttl: int = 300):
        self._cache: OrderedDict[int, tuple[object, float]] = OrderedDict()
        self._max_size = max_size
        self._ttl = ttl
        self._lock = threading.Lock()

    def get(self, pokemon_id: int) -> Optional[object]:
        with self._lock:
            if pokemon_id not in self._cache:
                return None
            _, expiry = self._cache[pokemon_id]
            if time.time() > expiry:
                del self._cache[pokemon_id]
                return None
            self._cache.move_to_end(pokemon_id)
            return self._cache[pokemon_id][0]

    def set(self, pokemon_id: int, pokemon: object) -> None:
        if pokemon is None:
            raise ValueError("pokemon cannot be None")
        with self._lock:
            if len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)  # evict LRU
            self._cache[pokemon_id] = (pokemon, time.time() + self._ttl)

    def invalidate(self, pokemon_id: int) -> None:
        with self._lock:
            self._cache.pop(pokemon_id, None)
