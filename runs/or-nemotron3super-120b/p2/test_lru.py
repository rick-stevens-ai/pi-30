import pytest
from lru import LRUCache

def test_basic_operations():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1       # returns 1
    cache.put(3, 3)                # evicts key 2
    assert cache.get(2) is None    # returns None (not found)
    cache.put(4, 4)                # evicts key 1
    assert cache.get(1) is None    # returns None (not found)
    assert cache.get(3) == 3       # returns 3
    assert cache.get(4) == 4       # returns 4

def test_update_existing_key():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)   # update existing key
    assert cache.get(1) == 10
    # After updating key 1, it becomes MRU. Key 2 is LRU.
    # Adding a new key should evict the LRU (key 2)
    cache.put(3, 3)
    assert cache.get(2) is None
    assert cache.get(3) == 3
    assert cache.get(1) == 10

def test_cache_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    assert cache.get(1) == 1
    cache.put(2, 2)
    assert cache.get(1) is None
    assert cache.get(2) == 2

def test_get_nonexistent():
    cache = LRUCache(2)
    assert cache.get(1) is None

def test_empty_cache():
    cache = LRUCache(0)
    cache.put(1, 1)
    assert cache.get(1) is None

def test_order_after_get():
    cache = LRUCache(3)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    # Access key 1 to make it most recently used
    assert cache.get(1) == 1
    # Add new key, should evict 2 (least recently used)
    cache.put(4, 4)
    assert cache.get(2) is None
    assert cache.get(1) == 1
    assert cache.get(3) == 3
    assert cache.get(4) == 4

def test_update_and_order():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    # Access 1
    cache.get(1)
    # Update 2 (should move to head)
    cache.put(2, 20)
    # Add 3, should evict 1? Wait: order after get(1): 1 is MRU, then 2 is LRU.
    # Then update 2: 2 becomes MRU, order: 2 (MRU), 1 (LRU)
    # Adding 3 evicts 1 (LRU)
    cache.put(3, 3)
    assert cache.get(1) is None
    assert cache.get(2) == 20
    assert cache.get(3) == 3

if __name__ == "__main__":
    pytest.main([__file__])