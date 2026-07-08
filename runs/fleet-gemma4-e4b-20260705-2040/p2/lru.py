from collections import OrderedDict
from typing import Any, Optional

class LRUCache:
    """
    An implementation of a Least Recently Used (LRU) Cache.
    Uses OrderedDict for O(1) average time complexity for get and put operations.
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        # OrderedDict maintains insertion order. We will use it to track recency.
        # The most recently used item is moved to the end upon access/update.
        self.cache = OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        """
        Retrieves an item from the cache. If found, updates its usage (recency).
        Returns the value if present, otherwise None. O(1) average time complexity.
        """
        if key not in self.cache:
            return None

        # Get the value
        value = self.cache[key]
        
        # Update recency by moving it to the end of the OrderedDict
        self.cache.move_to_end(key)
        
        return value

    def put(self, key: Any, value: Any):
        """
        Inserts or updates an item in the cache. Handles eviction if capacity is exceeded. O(1) average time complexity.
        If the key exists, its value is updated and it is marked as most recently used.
        If it's a new key, it's added, and eviction happens if necessary.
        """
        if key in self.cache:
            # Key exists: update value and refresh recency
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            # New key
            if len(self.cache) >= self.capacity:
                # Evict the least recently used item (the first item in OrderedDict)
                # last=False ensures FIFO/LRU behavior on popitem
                lru_key, _ = self.cache.popitem(last=False)
                # print(f"Evicted key: {lru_key}") # Optional logging for testing
            
            # Add the new item (it becomes the most recently used)
            self.cache[key] = value

# Example usage (optional, but good practice)
if __name__ == '__main__':
    cache = LRUCache(2)
    cache.put('a', 1)
    cache.put('b', 2)
    print(f"Get 'a': {cache.get('a')}") # returns 1, 'a' is now MRU
    cache.put('c', 3) # capacity exceeded, 'b' should be evicted (LRU)
    print("Cache keys after eviction:", list(cache.cache.keys())) # Should be ['a', 'c']
    print(f"Get 'b': {cache.get('b')}") # returns None
    cache.put('d', 4) # capacity exceeded, 'a' should be evicted (LRU)
    print("Cache keys after eviction:", list(cache.cache.keys())) # Should be ['c', 'd']
    print(f"Get 'c': {cache.get('c')}") # returns 3, 'c' is now MRU
