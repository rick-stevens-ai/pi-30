import pytest
from lru import LRUCache

def test_basic_put_get():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    assert cache.get(1) == "a"
    assert cache.get(2) == "b"

def test_eviction():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.put(3, "c")  # Evicts 1
    assert cache.get(1) is None
    assert cache.get(2) == "b"
    assert cache.get(3) == "c"

def test_get_updates_recency():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    # Access 1 to make it most recent
    assert cache.get(1) == "a"
    # Put 3, should evict 2 instead of 1
    cache.put(3, "c")
    assert cache.get(2) is None
    assert cache.get(1) == "a"
    assert cache.get(3) == "c"

def test_put_updates_value_and_recency():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    # Update 1's value and recency
    cache.put(1, "new_a")
    # Put 3, should evict 2
    cache.put(3, "c")
    assert cache.get(2) is None
    assert cache.get(1) == "new_a"
    assert cache.get(3) == "c"

def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, "a")
    assert cache.get(1) == "a"
    cache.put(2, "b")
    assert cache.get(1) is None
    assert cache.get(2) == "b"

def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-1)
