"""
LRU Cache implementation with O(1) operations.
Uses a doubly-linked list combined with a hash map for constant-time access.
"""
from collections import OrderedDict


class LRUCache:
    """
    LRU (Least Recently Used) Cache with O(1) get and put operations.
    
    Args:
        capacity: Maximum number of items the cache can hold.
    
    Methods:
        get(key): Retrieve value by key, returns None if not found.
        put(key, value): Insert or update key-value pair.
    """
    
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._cache = OrderedDict()
    
    def get(self, key):
        """
        Retrieve value by key. Marks the key as recently used.
        
        Args:
            key: The key to look up.
            
        Returns:
            The value associated with the key, or None if not found.
        """
        if key not in self._cache:
            return None
        # Move to end (most recently used)
        self._cache.move_to_end(key)
        return self._cache[key]
    
    def put(self, key, value):
        """
        Insert or update a key-value pair. Marks the key as recently used.
        If the cache is at capacity, evicts the least recently used item.
        
        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
        """
        if key in self._cache:
            # Update value and move to end
            self._cache.move_to_end(key)
            self._cache[key] = value
        else:
            # Insert new key
            self._cache[key] = value
            # Evict LRU if over capacity
            if len(self._cache) > self._capacity:
                self._cache.popitem(last=False)
    
    def __len__(self):
        """Return the current number of items in the cache."""
        return len(self._cache)
    
    def __contains__(self, key):
        """Check if key is in the cache."""
        return key in self._cache