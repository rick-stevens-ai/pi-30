import pytest
from lru import LRUCache


def test_get_missing():
    cache = LRUCache(2)
    assert cache.get(1) is None


def test_put_get():
    cache = LRUCache(2)
    cache.put(1, 1)
    assert cache.get(1) == 1


def test_eviction():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    assert cache.get(1) is None
    assert cache.get(2) == 2
    assert cache.get(3) == 3


def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)
    assert cache.get(2) is None
    assert cache.get(1) == 1


def test_put_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)
    cache.put(3, 3)
    assert cache.get(2) is None
    assert cache.get(1) == 10


def test_update_value():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(1, 10)
    assert cache.get(1) == 10


def test_capacity_zero():
    cache = LRUCache(0)
    cache.put(1, 1)
    assert cache.get(1) is None


def test_large_capacity():
    cache = LRUCache(1000)
    for i in range(1000):
        cache.put(i, i)
    for i in range(1000):
        assert cache.get(i) == i
