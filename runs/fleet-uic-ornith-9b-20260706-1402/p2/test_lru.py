import pytest
from typing import Optional
from lru import LRUCache


class TestLRUCache:
    """Tests for the LRU Cache implementation."""

    # ---- Basic operations -------------------------------------------------

    def test_get_missing_key_returns_none(self):
        cache = LRUCache(2)
        assert cache.get("a") is None

    def test_put_and_get(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        assert cache.get("a") == 1

    def test_put_overwrites_existing_value_refreshes_recency(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        # Updating "a" should refresh its recency so it's not evicted
        cache.put("a", 10)
        assert cache.get("a") == 10
        assert cache.get("b") == 2

    def test_get_refreshes_recency(self):
        """get() counts as a use — accessed items are promoted to MRU."""
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)

        # Access "a" so it becomes most recent
        cache.get("a")

        # Now put "d" — should evict "b" (least recently used), not "a" or "c"
        cache.put("d", 4)

        assert cache.get("a") == 1
        assert cache.get("b") is None   # evicted
        assert cache.get("c") == 3
        assert cache.get("d") == 4


    # ---- Eviction behavior ------------------------------------------------

    def test_evicts_lru_on_full_cache(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)   # evicts "a" (LRU)
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_eviction_order_with_interleaved_gets(self):
        """Verify that interleaved gets correctly change eviction order."""
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")       # "a" is now MRU, "b" is LRU
        cache.put("c", 3)    # evicts "b"
        assert cache.get("b") is None
        assert cache.get("c") == 3

    def test_multiple_evictions(self):
        """Repeated put operations beyond capacity should keep only the most recent."""
        cache = LRUCache(2)
        for i in range(5):
            cache.put(f"key{i}", i)
        # Only key3 and key4 remain
        assert cache.get("key0") is None
        assert cache.get("key1") is None
        assert cache.get("key2") is None
        assert cache.get("key3") == 3
        assert cache.get("key4") == 4

    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put("a", 1)
        assert cache.get("a") == 1
        cache.put("b", 2)   # evicts "a"
        assert cache.get("a") is None
        assert cache.get("b") == 2


    # ---- Edge cases -------------------------------------------------------

    def test_empty_cache(self):
        cache = LRUCache(3)
        assert len(cache.cache) == 0

    def test_put_updates_existing_key_without_eviction(self):
        """Putting a key that already exists should not increase size."""
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 99)   # overwrite, no eviction
        assert len(cache.cache) == 2

    def test_values_can_be_any_object(self):
        """Cache should handle non-integer values."""
        cache = LRUCache(1)
        cache.put("a", [1, 2])
        assert cache.get("a") == [1, 2]

    def test_put_with_none_value(self):
        cache = LRUCache(2)
        cache.put("a", None)
        assert cache.get("a") is None

    def test_put_with_none_value(self):
        cache = LRUCache(2)
        cache.put("a", None)
        assert cache.get("a") is None
