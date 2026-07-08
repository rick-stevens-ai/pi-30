import pytest
from lru import LRUCache


class TestLRUCache:
    def test_basic_get_put(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        assert cache.get("a") == 1
    
    def test_get_missing_key(self):
        cache = LRUCache(2)
        assert cache.get("missing") is None
    
    def test_lru_eviction(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # Should evict "a"
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3
    
    def test_get_refreshes_recency(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # "a" becomes most recently used
        cache.put("c", 3)  # Should evict "b", not "a"
        assert cache.get("a") == 1
        assert cache.get("b") is None
        assert cache.get("c") == 3
    
    def test_put_updates_existing_key(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 10)  # Update "a" and refresh recency
        cache.put("c", 3)  # Should evict "b", not "a"
        assert cache.get("a") == 10
        assert cache.get("b") is None
        assert cache.get("c") == 3
    
    def test_put_same_key_no_capacity_increase(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("a", 2)
        cache.put("a", 3)
        assert len(cache._cache) == 1
        assert cache.get("a") == 3
    
    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put("a", 1)
        assert cache.get("a") == 1
        cache.put("b", 2)  # Evicts "a"
        assert cache.get("a") is None
        assert cache.get("b") == 2
    
    def test_invalid_capacity(self):
        with pytest.raises(ValueError):
            LRUCache(0)
        with pytest.raises(ValueError):
            LRUCache(-1)
    
    def test_multiple_evictions(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.put("d", 4)  # Evicts "a"
        cache.put("e", 5)  # Evicts "b"
        assert cache.get("a") is None
        assert cache.get("b") is None
        assert cache.get("c") == 3
        assert cache.get("d") == 4
        assert cache.get("e") == 5
    
    def test_lru_order_after_multiple_gets(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.get("a")  # Order now: b, c, a
        cache.get("b")  # Order now: c, a, b
        cache.put("d", 4)  # Evicts "c"
        assert cache.get("c") is None
        assert cache.get("a") == 1
        assert cache.get("b") == 2
        assert cache.get("d") == 4