from collections import OrderedDict
from typing import Optional


class LRUCache:
    """Least-Recently-Used cache with O(1) get/put using OrderedDict."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: object) -> Optional[object]:
        if key not in self.cache:
            return None
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: object, value: object) -> None:
        if key in self.cache:
            # Update value and refresh recency
            self.cache.move_to_end(key)
            self.cache[key] = value
        else:
            # Evict LRU item if at capacity
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)  # Remove oldest (first)
            self.cache[key] = value
