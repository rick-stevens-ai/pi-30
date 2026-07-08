import pytest
from lru import LRUCache

def test_basic_put_get():
    cache = LRUCache(2)
    cache.put(1, "one")
    cache.put(2, "two")
    assert cache.get(1) == "one"
    assert cache.get(2) == "two"

def test_eviction():
    cache = LRUCache(2)
    cache.put(1, "one")
    cache.put(2, "two")
    cache.put(3, "three") # Evicts 1
    assert cache.get(1) is None
    assert cache.get(2) == "two"
    assert cache.get(3) == "three"

def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, "one")
    cache.put(2, "two")
    # Access 1, making it most recent
    cache.get(1)
    # Put 3, should evict 2 (least recent)
    cache.put(3, "three")
    assert cache.get(2) is None
    assert cache.get(1) == "one"
    assert cache.get(3) == "three"

def test_put_updates_value_and_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, "one")
    cache.put(2, "two")
    # Update 1, making it most recent and changing value
    cache.put(1, "updated one")
    # Put 3, should evict 2
    cache.put(3, "three")
    assert cache.get(2) is None
    assert cache.get(1) == "updated one"
    assert cache.get(3) == "three"

def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, "one")
    assert cache.get(1) == "one"
    cache.put(2, "two")
    assert cache.get(1) is None
    assert cache.get(2) == "two"

def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-1)
