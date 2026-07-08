"""Least Recently Used (LRU) cache implementation.

The LRUCache class provides O(1) operations for get and put using an OrderedDict.
This module only relies on the Python standard library.
"""

from collections import OrderedDict


class LRUCache:
    """Simple LRU cache with a fixed capacity.

    Parameters
    ----------
    capacity : int
        Maximum number of items that can be stored in the cache. If ``capacity`` is
        zero, all operations will act as no‑ops and ``get`` always returns
        ``None``.
    """

    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("Capacity must be non‑negative")
        self.capacity = capacity
        # The OrderedDict keeps the order of insertion/access; the last element is
        # the most recently used. Keys that are accessed via ``get`` or updated
        # via ``put`` are moved to the end.
        self.cache: OrderedDict[int, object] = OrderedDict()

    def get(self, key):
        """Return the value associated with *key* if present; otherwise ``None``.

        The key becomes the most recently used item.
        """
        if key not in self.cache:
            return None
        # Move to end (most recent)
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key, value):
        """Insert or update *key* with *value*.

        If the key already exists its value is overwritten and it becomes the most
        recently used. When inserting a new item and capacity exceeded, the least
        recently used item (the first element) is evicted.
        """
        if self.capacity == 0:
            return
        if key in self.cache:
            # Update value & move to end
            self.cache.pop(key)
            self.cache[key] = value
        else:
            if len(self.cache) >= self.capacity:
                # evict least recently used (first item)
                self.cache.popitem(last=False)
            self.cache[key] = value

    def __repr__(self):  # pragma: no cover - debugging aid
        return f"LRUCache(capacity={self.capacity}, cache={list(self.cache.items())})"
