"""Tests for lru.py — run with pytest."""

import pytest
from lru import LRUCache


# ---------------------------------------------------------------------------
# Basic capacity & eviction
# ---------------------------------------------------------------------------

def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, "a")
    assert cache.get(1) == "a"
    cache.put(2, "b")
    assert cache.get(1) is None  # evicted
    assert cache.get(2) == "b"


def test_put_evicts_lru():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.put(3, "c")  # evicts key 1
    assert cache.get(1) is None
    assert cache.get(2) == "b"
    assert cache.get(3) == "c"


def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.get(1)  # access 1, making 2 the LRU
    cache.put(3, "c")  # evicts key 2
    assert cache.get(1) == "a"
    assert cache.get(2) is None
    assert cache.get(3) == "c"


def test_put_existing_key_updates_value_and_recency():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.put(1, "a_new")  # updates value and refreshes recency
    cache.put(3, "c")  # evicts key 2 (now the LRU)
    assert cache.get(1) == "a_new"
    assert cache.get(2) is None
    assert cache.get(3) == "c"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_get_missing_key():
    cache = LRUCache(3)
    assert cache.get(99) is None


def test_overwrite_existing_key():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(1, "b")
    assert cache.get(1) == "b"


def test_capacity_one_overwrite():
    cache = LRUCache(1)
    cache.put(1, "a")
    cache.put(1, "b")
    assert cache.get(1) == "b"


def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)

    with pytest.raises(ValueError):
        LRUCache(-1)


# ---------------------------------------------------------------------------
# Larger stress test
# ---------------------------------------------------------------------------

def test_sequential_insertion():
    cache = LRUCache(3)
    for i in range(10):
        cache.put(i, i * 10)
    # Only last 3 should remain
    for i in range(7):
        assert cache.get(i) is None
    assert cache.get(7) == 70
    assert cache.get(8) == 80
    assert cache.get(9) == 90


def test_interleaved_access():
    cache = LRUCache(3)
    cache.put(1, 10)
    cache.put(2, 20)
    cache.put(3, 30)
    cache.get(1)  # 1 is most recent
    cache.put(4, 40)  # evicts 2 (LRU)
    assert cache.get(2) is None
    assert cache.get(1) == 10
    assert cache.get(3) == 30
    assert cache.get(4) == 40
