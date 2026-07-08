"""Least Recently Used (LRU) cache with O(1) get and put."""

from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    """LRU cache evicting the least recently used item on capacity overflow."""

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._cache = OrderedDict()

    def get(self, key) -> Optional[Any]:
        """Return the value for *key*, or None if absent.

        Accessing a key counts as "use" and moves it to the most-recent end.
        """
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: Any, value: Any) -> None:
        """Insert or update *key* with *value*.

        If the cache is full, the least recently used entry is evicted first.
        Updating an existing key also refreshes its recency.
        """
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self._capacity:
            self._cache.popitem(last=False)
