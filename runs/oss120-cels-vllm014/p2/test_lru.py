"""pytest suite for the LRUCache implementation.

The tests cover the basic contract required by the problem statement and
exercise a few edge‑cases (capacity of one, updating existing keys, etc.).
"""

import pytest

from lru import LRUCache


def test_basic_eviction():
    cache = LRUCache(2)
    cache.put(1, "one")
    cache.put(2, "two")
    assert cache.get(1) == "one"  # 1 becomes most‑recent
    cache.put(3, "three")        # should evict key 2
    assert cache.get(2) is None
    assert cache.get(1) == "one"
    assert cache.get(3) == "three"
    cache.put(4, "four")         # evicts key 1 (3 was just used)
    assert cache.get(1) is None
    assert cache.get(3) == "three"
    assert cache.get(4) == "four"


def test_update_refreshes():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    # update existing key – should refresh recency
    cache.put("a", 10)
    cache.put("c", 3)  # evicts "b"
    assert cache.get("b") is None
    assert cache.get("a") == 10
    assert cache.get("c") == 3


def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, "first")
    assert cache.get(1) == "first"
    cache.put(2, "second")  # evicts key 1
    assert cache.get(1) is None
    assert cache.get(2) == "second"


def test_missing_key_returns_none():
    cache = LRUCache(3)
    assert cache.get("missing") is None
    cache.put("x", 5)
    assert cache.get("y") is None


def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-1)
