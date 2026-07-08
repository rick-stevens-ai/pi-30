import pytest
from lru import LRUCache

def test_get_missing():
    cache = LRUCache(2)
    assert cache.get(1) is None

def test_put_and_get_updates():
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    assert cache.get(1) == 10
    assert cache.get(2) == 20
    # Access key 1 to refresh recency
    cache.get(1)
    # Now put new key should evict least recent (key 2)
    cache.put(3, 30)
    assert cache.get(2) is None
    assert cache.get(3) == 30

def test_put_updates_existing_key_refreshes():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 100)  # update existing key
    assert cache.get(1) == 100
    # After updating, the least recent is now key 2
    cache.put(3, 3)
    assert cache.get(2) is None
    assert cache.get(3) == 3

def test_capacity_zero():
    cache = LRUCache(0)
    cache.put(1, 1)
    assert cache.get(1) is None

def test_lru_eviction_order():
    cache = LRUCache(2)
    cache.put('a', 1)
    cache.put('b', 2)
    cache.get('a') # refresh a
    cache.put('c', 3)
    assert cache.get('a') == 1   # should still be present (most recent)
    assert cache.get('b') is None  # evicted

def test_put_on_full_capacity_evicts_oldest():
    cache = LRUCache(2)
    cache.put('x', 10)
    cache.put('y', 20)
    # Both inserted, order: x (oldest), y (most recent)
    assert cache.get('x') == 10
    assert cache.get('y') == 20
    # Access 'x' to make it most recent
    cache.get('x')
    # Now put new key should evict 'y' (least recent)
    cache.put('z', 30)
    assert cache.get('y') is None
    assert cache.get('z') == 30