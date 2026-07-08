from collections import OrderedDict
from typing import Any, Optional

class LRUCache:
    def __init__(self, capacity: int):
        """Initialize the LRU cache with a given capacity."""
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        """Retrieve the value for the given key and update its recency."""
        if key not in self.cache:
            return None
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> None:
        """Insert or update the key-value pair and update its recency."""
        if key in self.cache:
            # Update existing key's value and move to end
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                # Evict the least recently used (first item in OrderedDict)
                self.cache.popitem(last=False)
            self.cache[key] = value
            # New items are added to the end by default in OrderedDict
