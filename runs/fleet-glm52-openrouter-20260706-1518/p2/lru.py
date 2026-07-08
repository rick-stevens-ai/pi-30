"""O(1) LRU cache using OrderedDict (stdlib only)."""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self.capacity = capacity
        self._data: "OrderedDict[object, object]" = OrderedDict()

    def get(self, key):
        if key not in self._data:
            return None
        # Move to end = most recently used.
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key, value):
        if key in self._data:
            # Update value and refresh recency.
            self._data[key] = value
            self._data.move_to_end(key)
            return
        if self.capacity == 0:
            return
        if len(self._data) >= self.capacity:
            # Evict least recently used = first item.
            self._data.popitem(last=False)
        self._data[key] = value
