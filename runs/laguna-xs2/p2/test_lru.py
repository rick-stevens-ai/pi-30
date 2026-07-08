"""
Tests for LRUCache implementation.
"""
import pytest
from lru import LRUCache


class TestLRUCacheBasic:
    """Basic functionality tests."""
    
    def test_init_positive_capacity(self):
        """Cache initializes with positive capacity."""
        cache = LRUCache(5)
        assert len(cache) == 0
    
    def test_init_zero_capacity_raises(self):
        """Zero capacity raises ValueError."""
        with pytest.raises(ValueError, match="Capacity must be positive"):
            LRUCache(0)
    
    def test_init_negative_capacity_raises(self):
        """Negative capacity raises ValueError."""
        with pytest.raises(ValueError, match="Capacity must be positive"):
            LRUCache(-1)
    
    def test_get_missing_key_returns_none(self):
        """Getting a missing key returns None."""
        cache = LRUCache(2)
        assert cache.get("missing") is None
    
    def test_put_and_get(self):
        """Put and get a single item."""
        cache = LRUCache(2)
        cache.put("a", 1)
        assert cache.get("a") == 1
    
    def test_contains(self):
        """Test __contains__ operator."""
        cache = LRUCache(2)
        cache.put("a", 1)
        assert "a" in cache
        assert "b" not in cache


class TestLRUCacheEviction:
    """Test LRU eviction behavior."""
    
    def test_eviction_order(self):
        """Evict least recently used item when at capacity."""
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # Should evict "a"
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3
    
    def test_get_refreshes_recency(self):
        """Accessing an item via get refreshes its recency."""
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # "a" is now most recently used
        cache.put("c", 3)  # Should evict "b", not "a"
        assert cache.get("a") == 1
        assert cache.get("b") is None
        assert cache.get("c") == 3
    
    def test_put_updates_value_and_refreshes_recency(self):
        """Putting on existing key updates value and refreshes recency."""
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 10)  # Update "a" and make it most recent
        cache.put("c", 3)  # Should evict "b", not "a"
        assert cache.get("a") == 10
        assert cache.get("b") is None
        assert cache.get("c") == 3
    
    def test_put_existing_key_no_eviction(self):
        """Putting existing key doesn't cause eviction."""
        cache = LRUCache(1)
        cache.put("a", 1)
        cache.put("a", 2)  # Update, not insert
        assert len(cache) == 1
        assert cache.get("a") == 2


class TestLRUCacheEdgeCases:
    """Edge case tests."""
    
    def test_none_key(self):
        """None can be a key."""
        cache = LRUCache(2)
        cache.put(None, "null_key")
        assert cache.get(None) == "null_key"
    
    def test_none_value(self):
        """None can be a value."""
        cache = LRUCache(2)
        cache.put("a", None)
        assert cache.get("a") is None
        # Distinguish between "not found" and "value is None"
        # This is expected behavior for this implementation
    
    def test_various_value_types(self):
        """Cache can store various value types."""
        cache = LRUCache(4)
        cache.put("int", 42)
        cache.put("str", "hello")
        cache.put("list", [1, 2, 3])
        cache.put("dict", {"key": "value"})
        
        assert cache.get("int") == 42
        assert cache.get("str") == "hello"
        assert cache.get("list") == [1, 2, 3]
        assert cache.get("dict") == {"key": "value"}
    
    def test_capacity_one(self):
        """Cache with capacity 1."""
        cache = LRUCache(1)
        cache.put("a", 1)
        assert cache.get("a") == 1
        cache.put("b", 2)  # Evicts "a"
        assert cache.get("a") is None
        assert cache.get("b") == 2


class TestLRUCacheMultipleEvictions:
    """Test multiple eviction scenarios."""
    
    def test_multiple_evictions(self):
        """Multiple evictions work correctly."""
        cache = LRUCache(3)
        for i in range(10):
            cache.put(i, i * 10)
        
        # Only last 3 items should remain
        assert cache.get(7) == 70
        assert cache.get(8) == 80
        assert cache.get(9) == 90
        
        # Earlier items should be evicted
        for i in range(7):
            assert cache.get(i) is None
    
    def test_repeated_access_pattern(self):
        """Test complex access patterns."""
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.get("a")  # a is MRU
        cache.put("d", 4)  # evicts b
        cache.get("c")  # c is MRU
        cache.put("e", 5)  # evicts d (not in cache), so evicts a? No, b was evicted
        # Order: b evicted, then d inserted, then c accessed, then e inserted
        # Current: a, c, d, e - capacity 3, so evict d
        # Let me trace again:
        # a, b, c -> get a -> a, c, b (a MRU)
        # put d -> evicts b -> a, c, d (b gone)
        # get c -> c, d, a (c MRU)
        # put e -> evicts a -> c, d, e (a gone)
        assert cache.get("a") is None  # evicted
        assert cache.get("b") is None  # evicted earlier
        assert cache.get("c") == 3
        assert cache.get("d") == 4
        assert cache.get("e") == 5