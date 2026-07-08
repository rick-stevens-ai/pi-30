from collections import OrderedDict


class LRUCache:
    """LRU cache with O(1) get/put via OrderedDict."""

    def __init__(self, capacity: int):
        self.capacity = max(int(capacity), 0) if capacity is not None and capacity > 0 else float('inf')
        self.cache = OrderedDict()

    def get(self, key: object) -> object:
        if key not in self.cache:
            return None
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key: object, value: object):
        if key in self.cache:
            self.cache.pop(key)
            self.cache[key] = value
        else:
            # Need to insert and potentially evict.
            # Check if a different key exists that would be evicted.
            if len(self.cache) >= self.capacity and self._has_key_to_evict():
                pass  # will fall through to normal insert with eviction logic below
            self.cache[key] = value
