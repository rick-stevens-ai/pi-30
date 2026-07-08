import pytest
from lru import LRUCache


def test_basic_put_and_get():
    cache = LRUCache(2)
    cache.put('a', 1)
    cache.put('b', 2)
    assert cache.get('a') == 1
    assert cache.get('b') == 2
    # non‑existent key returns None
    assert cache.get('c') is None


def test_lru_eviction_order():
    cache = LRUCache(2)
    cache.put('a', 1)  # a is MRU
    cache.put('b', 2)  # b is MRU, a is LRU
    # Access 'a' makes it MRU, 'b' becomes LRU
    assert cache.get('a') == 1
    cache.put('c', 3)  # should evict 'b'
    assert cache.get('b') is None
    assert cache.get('a') == 1
    assert cache.get('c') == 3


def test_put_updates_existing_and_refreshes():
    cache = LRUCache(2)
    cache.put('x', 10)
    cache.put('y', 20)
    # Update 'x' value and refresh recency
    cache.put('x', 15)
    # 'y' should now be LRU
    cache.put('z', 30)  # evicts 'y'
    assert cache.get('y') is None
    assert cache.get('x') == 15
    assert cache.get('z') == 30


def test_capacity_one_eviction():
    cache = LRUCache(1)
    cache.put('first', 1)
    assert cache.get('first') == 1
    cache.put('second', 2)
    # The first entry must be gone
    assert cache.get('first') is None
    assert cache.get('second') == 2


def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
