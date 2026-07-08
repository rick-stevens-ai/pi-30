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
    cache.put(3, "c")  # Should evict 1
    assert cache.get(1) is None
    assert cache.get(2) == "b"
    assert cache.get(3) == "c"

def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.get(1)       # 1 is now most recent, 2 is least recent
    cache.put(3, "c")  # Should evict 2
    assert cache.get(2) is None
    assert cache.get(1) == "a"
    assert cache.get(3) == "c"

def test_put_existing_key_updates_and_refreshes():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.put(1, "updated_a") # 1 is most recent, 2 is least recent
    cache.put(3, "c")        # Should evict 2
    assert cache.get(2) is None
    assert cache.get(1) == "updated_a"
    assert cache.get(3) == "c"

def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, "a")
    assert cache.get(1) == "a"
    cache.put(2, "b")
    assert cache.get(1) is None
    assert cache.get(2) == "b"

def test_get_non_existent():
    cache = LRUCache(2)
    assert cache.get(99) is None

def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-1)
