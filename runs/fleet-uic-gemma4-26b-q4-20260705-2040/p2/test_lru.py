import pytest
from lru import LRUCache

def test_basic_operations():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # evicts 2
    assert cache.get(2) is None
    assert cache.get(3) == 3
    assert cache.get(1) == 1

def test_update_existing_key():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)  # updates value and refreshes recency
    cache.put(3, 3)   # evicts 2 because 1 was refreshed
    assert cache.get(1) == 10
    assert cache.get(2) is None
    assert cache.get(3) == 3

def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) is None
    assert cache.get(2) == 2

def test_get_nonexistent():
    cache = LRUCache(2)
    assert cache.get(99) is None

def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-1)

def test_recency_on_put():
    cache = LRUCache(3)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    # Order is 1, 2, 3 (3 is most recent)
    cache.get(1) # Order: 2, 3, 1 (1 is most recent)
    cache.put(4, 4) # evicts 2
    assert cache.get(2) is None
    assert cache.get(1) == 1
    assert cache.get(3) == 3
    assert cache.get(4) == 4

def test_recency_on_update():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    # Order: 1, 2
    cache.put(1, 10) # Update 1, order becomes: 2, 1
    cache.put(3, 3)  # evicts 2
    assert cache.get(2) is None
    assert cache.get(1) == 10
    assert cache.get(3) == 3

if __name__ == "__main__":
    pytest.main([__file__])
