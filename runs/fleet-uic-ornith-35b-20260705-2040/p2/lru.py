"""LRU Cache – O(1) get/put using stdlib OrderedDict."""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: "OrderedDict" = OrderedDict()

    def get(self, key):
        """Return value for *key* or None; counts as a use (refreshes recency)."""
        if key not in self.cache:
            return None
        # Move to end so it becomes most-recently-used.
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        """Insert/update *key* with *value*; refreshes recency.  Evicts LRU on overflow."""
        if key in self.cache:
            # Update and refresh.
            self.cache.move_to_end(key)
        else:
            # New entry – may need to evict the least-recently-used item.
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)  # pop oldest (first-inserted / LRU)
        self.cache[key] = value
