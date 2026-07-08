"""Pytest tests for LRU Cache implementation."""
import pytest
from lru import LRUCache


class TestLRUCache:
    def test_basic_put_get(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        assert cache.get("a") == 1

    def test_get_nonexistent(self):
        cache = LRUCache(2)
        assert cache.get("missing") is None

    def test_lru_eviction_on_put(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # Should evict "a" (LRU)
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_get_refreshes_recency(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # Access "a", making it most recent
        cache.put("c", 3)  # Should evict "b" (LRU), not "a"
        assert cache.get("a") == 1
        assert cache.get("b") is None
        assert cache.get("c") == 3

    def test_put_on_existing_updates_value_and_refreshes(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 10)  # Update "a" and refresh its recency
        cache.put("c", 3)  # Should evict "b" (LRU), not "a"
        assert cache.get("a") == 10
        assert cache.get("b") is None
        assert cache.get("c") == 3

    def test_multiple_accesses(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.get("a")  # a -> MRU
        cache.get("b")  # b -> MRU
        cache.put("d", 4)  # c is LRU, should be evicted
        assert cache.get("c") is None
        assert cache.get("a") == 1
        assert cache.get("b") == 2
        assert cache.get("d") == 4

    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put("a", 1)
        assert cache.get("a") == 1
        cache.put("b", 2)  # Evicts "a"
        assert cache.get("a") is None
        assert cache.get("b") == 2

    def test_capacity_zero_raises(self):
        with pytest.raises(ValueError):
            LRUCache(0)

    def test_capacity_negative_raises(self):
        with pytest.raises(ValueError):
            LRUCache(-1)

    def test_size_tracking(self):
        cache = LRUCache(3)
        assert len(cache) == 0
        cache.put("a", 1)
        assert len(cache) == 1
        cache.put("b", 2)
        assert len(cache) == 2
        cache.put("c", 3)
        assert len(cache) == 3
        cache.put("d", 4)  # Evicts one
        assert len(cache) == 3

    def test_contains(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        assert "a" in cache
        assert "b" not in cache

    def test_none_value_allowed(self):
        cache = LRUCache(2)
        cache.put("a", None)
        assert cache.get("a") is None  # Could be missing key or stored None

        # Distinguish: put a key, then check it exists
        cache.put("b", 1)
        assert "a" in cache  # "a" was explicitly put

    def test_update_without_eviction(self):
        """Updating existing key should not cause eviction."""
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 10)  # Update, no eviction
        assert len(cache) == 2
        assert cache.get("a") == 10
        assert cache.get("b") == 2

    def test_lru_order_after_mixed_operations(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.get("a")  # Order: b, c, a (a MRU)
        cache.put("d", 4)  # Evict b
        assert cache.get("b") is None
        cache.get("c")  # Order: a, d, c (c MRU)
        cache.put("e", 5)  # Evict a
        assert cache.get("a") is None
        assert cache.get("d") == 4
        assert cache.get("c") == 3
        assert cache.get("e") == 5