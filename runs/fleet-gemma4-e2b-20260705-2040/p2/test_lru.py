import pytest
from lru import LRUCache

def test_lru_basic_operations():
    """Tests basic put and get operations."""
    cache = LRUCache(2)
    
    # Test initial state
    assert cache.get(1) is None

    # Put 1
    cache.put(1, 10)
    assert cache.get(1) == 10
    
    # Put 2
    cache.put(2, 20)
    assert cache.get(2) == 20
    
    # Check capacity is full
    assert len(cache.cache) == 2

def test_lru_recency_update():
    """Tests that accessing an item refreshes its recency."""
    cache = LRUCache(2)
    
    cache.put(1, 100) # Order: [1]
    cache.put(2, 200) # Order: [1, 2] (2 is MRU)
    
    # Access key 1. It should move to the MRU position.
    assert cache.get(1) == 100 # Should return value
    
    # Now state should be: [2, 1] (1 is MRU)
    
    # Put a new item 3. Key 2 (the current LRU) should be evicted.
    cache.put(3, 300)
    
    assert cache.get(2) is None # Key 2 should be evicted
    assert cache.get(1) == 100 # Key 1 should still exist

def test_lru_update_value():
    """Tests that updating an existing key refreshes its recency."""
    cache = LRUCache(2)
    
    cache.put(1, 10) # Order: [1]
    cache.put(2, 20) # Order: [1, 2] (2 is MRU)
    
    # Update key 1. It should refresh recency and update value.
    cache.put(1, 100) # Order: [2, 1] (1 is MRU)
    
    # Put a new item 3. Key 2 (the current LRU) should be evicted.
    cache.put(3, 300)
    
    assert cache.get(2) is None # Key 2 evicted
    assert cache.get(1) == 100 # Updated value check
    assert cache.get(3) == 300

def test_lru_capacity_error():
    """Tests behavior with zero or negative capacity."""
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-5)