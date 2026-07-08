import pytest
from lru import LRUCache

def test_initialization():
    """Test cache initialization."""
    cache = LRUCache(3)
    assert cache.capacity == 3
    assert len(cache.cache) == 0

def test_put_and_get_basic():
    """Test basic put and get functionality."""
    cache = LRUCache(2)
    cache.put('a', 1)
    cache.put('b', 2)
    assert cache.get('a') == 1
    assert cache.get('b') == 2
    # Test non-existent key
    assert cache.get('c') is None

def test_lru_eviction():
    """Test LRU eviction logic."""
    cache = LRUCache(2)
    
    # Fill the cache: 'a' (LRU), 'b' (MRU)
    cache.put('a', 1)
    cache.put('b', 2)
    
    # Access 'a'. 'a' becomes MRU, 'b' becomes LRU.
    _ = cache.get('a')
    
    # Add 'c'. Since capacity is 2, the current LRU ('b') must be evicted.
    cache.put('c', 3)
    
    assert len(cache.cache) == 2
    # Check if 'b' was evicted
    assert cache.get('b') is None
    # Check if 'a' and 'c' are present
    assert cache.get('a') == 1
    assert cache.get('c') == 3

def test_put_updates_and_refreshes_recency():
    """Test updating an existing key refreshes its recency."""
    cache = LRUCache(2)
    # Initial state: 'a' (LRU), 'b' (MRU)
    cache.put('a', 1)
    cache.put('b', 2)
    
    # Update 'a'. It should remain in the cache, and become MRU.
    cache.put('a', 100) # New value for existing key
    
    # Add 'c'. Since capacity is 2, the current LRU ('b') must be evicted.
    cache.put('c', 3)
    
    assert len(cache.cache) == 2
    # Check if 'b' was evicted
    assert cache.get('b') is None
    # Check if updated 'a' and new 'c' are present
    assert cache.get('a') == 100
    assert cache.get('c') == 3

def test_put_on_empty_cache():
    """Test putting into an empty cache."""
    cache = LRUCache(1)
    cache.put('x', 99)
    assert cache.get('x') == 99
    
def test_capacity_zero_or_negative():
    """Test handling invalid capacity initialization."""
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-5)

# Test edge case where cache is exactly full and a new item is added (should evict LRU)
def test_capacity_full_eviction():
    cache = LRUCache(3)
    cache.put('k1', 1) # LRU: k1
    cache.put('k2', 2) # LRU: k1, MRU: k2
    cache.put('k3', 3) # LRU: k1, MRU: k3

    # Access k1 to make it MRU
    _ = cache.get('k1') # Order: k2 (LRU), k3, k1 (MRU)

    # Add k4. k2 should be evicted.
    cache.put('k4', 4)
    
    assert len(cache.cache) == 3
    assert cache.get('k2') is None # Should be evicted
    assert cache.get('k1') == 1
    assert cache.get('k3') == 3
    assert cache.get('k4') == 4