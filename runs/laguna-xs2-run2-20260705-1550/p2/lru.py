from collections import OrderedDict


class LRUCache:
    """LRU Cache implementation with O(1) get and put operations."""
    
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._cache = OrderedDict()
    
    def get(self, key):
        """Get value by key, returning None if not found.
        Also marks the key as recently used."""
        if key not in self._cache:
            return None
        # Move to end (most recently used)
        self._cache.move_to_end(key)
        return self._cache[key]
    
    def put(self, key, value):
        """Put key-value pair into cache.
        Updates value if key exists and marks as recently used."""
        if key in self._cache:
            # Update value and move to end
            self._cache[key] = value
            self._cache.move_to_end(key)
        else:
            # Add new entry
            self._cache[key] = value
            # Evict LRU if at capacity
            if len(self._cache) > self._capacity:
                self._cache.popitem(last=False)  # Remove least recently used