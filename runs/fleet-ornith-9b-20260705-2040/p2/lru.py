from collections import OrderedDict
from typing import Optional


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._cache = OrderedDict()

    def get(self, key: object) -> Optional[object]:
        if key not in self._cache:
            return None
        # Move to end (most recently used)
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: object, value: object) -> None:
        if key in self._cache:
            # Update value and refresh recency
            self._cache.move_to_end(key)
            self._cache[key] = value
        else:
            if len(self._cache) == self._capacity:
                # Evict least recently used (first item)
                self._cache.popitem(last=False)
            self._cache[key] = value
