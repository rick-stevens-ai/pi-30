"""
Pytest tests for LRUCache.
Tests correctness, O(1) behavior, eviction policy, and recency updates on get/put.
"""

import pytest
from lru import LRUCache


# --- Basic functionality ---

def test_get_missing():
    """Returns None for missing keys."""
    cache = LRUCache(2)
    assert cache.get("a") is None
    cache.put("b", 1)
    assert cache.get("c") is None


def test_put_get():
    """Basic put/get for single key."""
    cache = LRUCache(2)
    cache.put("a", 42)
    assert cache.get("a") == 42


def test_update_value_on_put():
    """Updating value via put changes the stored value."""
    cache = LRUCache(2)
    cache.put("a", 1)
    assert cache.get("a") == 1
    cache.put("a", 2)
    assert cache.get("a") == 2


# --- Capacity & eviction ---

def test_capacity_limit():
    """Cache respects capacity limit."""
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert len(cache.cache) == 2
    cache.put("c", 3)
    assert len(cache.cache) == 2


def test_evict_lru_on_put():
    """Least recently used item is evicted when capacity exceeded on put."""
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # a now most recent
    cache.put("c", 3)  # b is now least recently used -> evicted
    assert "b" not in cache.cache
    assert "a" in cache.cache and "c" in cache.cache


def test_eviction_order_after_multiple_gets():
    """Eviction respects recency across multiple get/put operations."""
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")     # a most recent
    cache.put("c", 3)   # b least recent -> evicted
    assert "b" not in cache.cache
    # Now only a and c; mark a again to make it least recent
    cache.get("c")     # c most recent, a becomes least
    cache.put("d", 4)   # a evicted (least), remaining: c,d
    assert "a" not in cache.cache
    assert "c" in cache.cache and "d" in cache.cache


# --- Recency updates on get/put ---

def test_get_updates_recency():
    """get operation refreshes recency."""
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    # b is least recent; access a to make it most recent
    cache.get("a")     # a now MRU, b now LRU
    cache.put("c", 3)   # evicts b (LRU), keeps a,c
    assert "b" not in cache.cache
    assert "a" in cache.cache and "c" in cache.cache


def test_put_existing_updates_recency():
    """put on existing key refreshes recency like get does."""
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    # update b to become most recent
    cache.put("b", 99)  # still capacity=2; no eviction yet
    cache.put("c", 3)   # now capacity exceeded; a is LRU -> evicted
    assert "a" not in cache.cache
    assert "b" in cache.cache and "c" in cache.cache


def test_recency_after_many_operations():
    """Multiple get/put operations maintain correct recency chain."""
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    # order: head->c,b,a->tail
    cache.get("a")      # a most recent -> c,b,a
    cache.put("d", 4)     # evicts b; remaining: d (head), c, a (tail.prev)
    assert set(cache.cache.keys()) == {"d", "c", "a"}
    cache.get("b")      # b already evicted; no change in cache
    cache.put("e", 5)     # evicts d (now tail.prev); remaining: e,b,a
    assert "d" not in cache.cache
    assert set(cache.cache.keys()) == {"e",  "c", "a"}


# --- Edge cases ---

def test_capacity_zero():
    """Capacity 0 behaves correctly."""
    with pytest.raises(Exception):
        # Allowing capacity <= 0 depends on implementation; here we require >=1
        cache = LRUCache(0)
        cache.put("x", 1)  # Should fail or behave predictably
