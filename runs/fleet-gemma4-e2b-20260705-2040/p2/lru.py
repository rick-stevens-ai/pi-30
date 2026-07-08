from collections import OrderedDict

class LRUCache:
    """
    A Least Recently Used (LRU) Cache implementation using OrderedDict.
    Provides O(1) time complexity for get and put operations,
    correctly handling LRU eviction based on usage.
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self.capacity = capacity
        # OrderedDict stores key-value pairs and maintains insertion/access order.
        # The front of the dictionary is the Most Recently Used (MRU),
        # and the end is the Least Recently Used (LRU).
        self.cache = OrderedDict()

    def get(self, key: int) -> int or None:
        """
        Retrieves an item from the cache. Moves the accessed item to the front (MRU).
        Returns the value or None if the key is not found.
        """
        if key not in self.cache:
            return None
        
        # Move the accessed item to the end (most recently used)
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key: int, value: int) -> None:
        """
        Inserts or updates an item in the cache. Handles eviction if capacity is exceeded.
        If the key exists, its value is updated and it becomes the MRU.
        """
        if key in self.cache:
            # Update value and move to the end (MRU)
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # Evict the LRU item (the first item in OrderedDict)
            # last=False means popitem(last=False) removes the first item (LRU)
            self.cache.popitem(last=False)
        
        # Insert the new item (it automatically becomes the MRU/end of the OrderedDict)
        self.cache[key] = value

def test_lru():
    """
    Tests for the LRUCache implementation using pytest.
    """
    capacity = 2
    cache = LRUCache(capacity)

    # Test 1: Basic put and get
    assert cache.get(1) is None
    cache.put(1, 1)
    assert cache.get(1) == 1
    
    # Test 2: Put another item
    cache.put(2, 2)
    assert cache.get(2) == 2
    
    # Test 3: Check capacity (Cache is full: {1, 2})
    assert cache.get(1) == 1 # Accessing 1 makes it MRU
    
    # Test 4: Eviction - Put a third item (3). 1 should be evicted as it is now LRU.
    cache.put(3, 3)
    assert cache.get(1) is None # 1 should be evicted
    assert cache.get(2) == 2 # 2 should still be present

    # Test 5: Update existing key (Recency refresh and value update)
    cache.put(2, 200) # Update value of 2, making it MRU
    # Current state: {2, 3}. 2 is MRU, 3 is LRU. Capacity is 2.
    
    # Test 6: Eviction again - Put a fourth item (4). 3 should be evicted as it is now LRU.
    cache.put(4, 4)
    assert cache.get(3) is None # 3 should be evicted
    assert cache.get(2) == 200 # Updated value check
    assert cache.get(4) == 4

    # Test 7: Non-existent key get
    assert cache.get(99) is None

    # Test 8: Capacity check with zero capacity (should raise ValueError during init, but we test for normal flow)
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-1)


if __name__ == '__main__':
    # This block is generally not needed when running via pytest, 
    # but kept for completeness if someone runs lru.py directly.
    print("Running tests...")
    test_lru()
    print("Tests finished.")