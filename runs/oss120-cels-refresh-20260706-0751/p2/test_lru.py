"""Tests for the LRUCache implementation in lru.py.

The tests cover basic insertion / retrieval, updating existing keys, LRU
eviction order and that both ``get`` and ``put`` refresh recency.
"""

import pytest

from lru import LRUCache


def test_basic_put_and_get():
    cache = LRUCache(capacity=2)
    assert cache.get("a") is None
    cache.put("a", 1)
    assert cache.get("a") == 1
    cache.put("b", 2)
    assert cache.get("b") == 2
    # Cache is full but no eviction yet
    assert len(cache) == 2


def test_update_existing_key_refreshes_recency():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    # Access "a" to make it most recent
    assert cache.get("a") == 1
    # Insert new key, should evict "b" (least recent)
    cache.put("c", 3)
    assert "b" not in cache
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_put_existing_key_updates_value_and_recency():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    # Update "a" with a new value
    cache.put("a", 10)
    assert cache.get("a") == 10
    # Now "b" is least recent; inserting "c" should evict "b"
    cache.put("c", 3)
    assert "b" not in cache
    assert cache.get("a") == 10
    assert cache.get("c") == 3


def test_capacity_one_eviction():
    cache = LRUCache(capacity=1)
    cache.put("x", 100)
    assert cache.get("x") == 100
    cache.put("y", 200)
    # "x" should be evicted because capacity is 1
    assert cache.get("x") is None
    assert cache.get("y") == 200


def test_invalid_capacity_raises():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-5)
