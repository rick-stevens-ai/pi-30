"""Pytest tests for LRUCache."""

import pytest

from lru import LRUCache


class TestBasic:
    def test_get_empty(self):
        cache = LRUCache(2)
        assert cache.get("a") is None

    def test_put_then_get(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        assert cache.get("a") == 1

    def test_get_nonexistent(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        assert cache.get("b") is None

    def test_len(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        assert len(cache) == 2

    def test_contains(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        assert "a" in cache
        assert "b" not in cache


class TestEviction:
    def test_evicts_lru_on_capacity(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        # "a" is now LRU
        cache.put("c", 3)
        assert cache.get("a") is None  # evicted
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_get_refreshes_recency(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        # touch "a" -> it's now most recent, "b" is LRU
        assert cache.get("a") == 1
        cache.put("c", 3)
        assert cache.get("a") == 1  # still present
        assert cache.get("b") is None  # evicted

    def test_put_existing_refreshes_recency(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        # update "a" -> it becomes MRU
        cache.put("a", 10)
        assert cache.get("a") == 10
        cache.put("c", 3)
        assert cache.get("a") == 10  # survived
        assert cache.get("b") is None  # evicted

    def test_put_existing_updates_value(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("a", 99)
        assert cache.get("a") == 99
        assert len(cache) == 1  # no duplicate / no growth

    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put("a", 1)
        assert cache.get("a") == 1
        cache.put("b", 2)
        assert cache.get("a") is None
        assert cache.get("b") == 2

    def test_capacity_zero_put_is_noop(self):
        cache = LRUCache(0)
        cache.put("a", 1)
        assert cache.get("a") is None
        assert len(cache) == 0

    def test_capacity_zero_get(self):
        cache = LRUCache(0)
        assert cache.get("anything") is None


class TestEdgeCases:
    def test_negative_capacity_raises(self):
        with pytest.raises(ValueError):
            LRUCache(-1)

    def test_overwrite_does_not_evict(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("a", 2)
        cache.put("a", 3)
        assert len(cache) == 1
        assert cache.get("a") == 3

    def test_long_chain_eviction_order(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        # access order: a,b,c -> c is MRU, a is LRU
        cache.get("a")  # a now MRU; order: b,c,a
        cache.put("d", 4)  # evict b
        assert cache.get("b") is None
        assert cache.get("a") == 1
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_put_existing_makes_mru_not_evicted(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        # update c -> c becomes MRU, a is LRU
        cache.put("c", 30)
        cache.put("d", 4)
        assert cache.get("a") is None  # evicted
        assert cache.get("c") == 30
        assert cache.get("d") == 4
        assert cache.get("b") == 2

    def test_integer_keys(self):
        cache = LRUCache(2)
        cache.put(1, "one")
        cache.put(2, "two")
        assert cache.get(1) == "one"
        cache.put(3, "three")
        assert cache.get(2) is None
        assert cache.get(1) == "one"

    def test_none_key(self):
        cache = LRUCache(2)
        cache.put(None, "v")
        assert cache.get(None) == "v"

    def test_none_value(self):
        cache = LRUCache(2)
        cache.put("k", None)
        assert cache.get("k") is None  # value is None but present

    def test_get_missing_does_not_affect_eviction(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("missing")  # should not change recency
        cache.put("c", 3)
        assert cache.get("a") is None  # evicted, "b" was LRU
        assert cache.get("b") == 2

    def test_repr(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        r = repr(cache)
        assert "LRUCache" in r
        assert "capacity=2" in r
        assert "size=1" in r


if __name__ == "__main__":
    pytest.main([__file__, "-v"])