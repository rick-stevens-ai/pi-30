"""
Simple LRU cache implementation.

The cache stores at most `capacity` items. The most recently accessed
(item used by `get` or inserted/updated by `put`) is moved to the
end of an internal `OrderedDict`. When the capacity is exceeded the
least recently used item (the first one) is evicted.

Only the standard library is used: `collections.OrderedDict`.
"""

from collections import OrderedDict


class LRUCache:
    """Very small LRU cache.

    Parameters
    ----------
    capacity:
        Maximum number of key/value pairs that can be held in the cache.
        A capacity of zero means the cache never stores anything.

    Methods
    -------
    get(key)
        Return the value for *key* or ``None`` if the key is not present.
        The key is marked as recently used.
    put(key, value)
        Insert or update a key/value pair. If the key already exists its
        value is overwritten and the key becomes most recently used.
        If the cache is full, the least recently used entry is evicted.
    """

    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("capacity must be non‑negative")
        self.capacity = capacity
        self._cache: OrderedDict = OrderedDict()

    def get(self, key):
        """Return the value for *key* or ``None`` if not present.

        Time complexity: O(1).
        """
        if key not in self._cache:
            return None
        # Move key to the end to mark it as recently used.
        value = self._cache.pop(key)
        self._cache[key] = value
        return value

    def put(self, key, value):
        """Insert or update the key/value pair.

        Evicts the least recently used item if capacity is exceeded.
        Time complexity: O(1).
        """
        if self.capacity == 0:
            return
        if key in self._cache:
            self._cache.pop(key)
        elif len(self._cache) == self.capacity:
            self._cache.popitem(last=False)
        self._cache[key] = value

    def __repr__(self):
        return f"LRUCache(capacity={self.capacity}, cache={list(self._cache.items())})"
