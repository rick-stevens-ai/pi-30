import pytest
from lru import LRUCache


class TestLRUCache:
    def test_basic_put_and_get(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.get("a") == 1
        assert cache.get("b") == 2

    def test_get_nonexistent_returns_none(self):
        cache = LRUCache(2)
        assert cache.get("x") == None

    def test_eviction_on_capacity_exceeded(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)            # all fit, no eviction yet
        cache.put("d", 4)            # evicts LRU "a"
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_get_refreshes_recency(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        # Access b to refresh recency
        cache.get("b")
        # Now a is least recently used, c was last accessed before put below
        cache.put("d", 4)
        assert cache.get("a") == None  # evicted
        assert cache.get("b") == 2
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_put_existing_key_updates_value_and_recency(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)            # all fit
        # Update a (existing key): refreshes recency, no eviction beyond cap
        cache.put("a", 10)
        assert cache.get("a") == 10
        assert len(cache._cache) == 3   # nothing evicted

    def test_put_existing_key_does_not_evict(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        # Reputing an existing key should not cause eviction beyond capacity
        cache.put("a", 10)
        assert len(cache._cache) == 3

    def test_capacity_1(self):
        cache = LRUCache(1)
        cache.put("x", 99)
        assert cache.get("x") == 99
        cache.put("y", 88)
        assert cache.get("x") == None
        assert cache.get("y") == 88

    def test_empty_cache(self):
        cache = LRUCache(5)
        assert cache.get("anything") == None
        cache.put("k", "v")
        assert cache.get("k") == "v"

    def test_large_capacity(self):
        cache = LRUCache(100)
        for i in range(100):
            cache.put(i, i * 2)
        # All should be present
        for i in range(100):
            assert cache.get(i) == i * 2
