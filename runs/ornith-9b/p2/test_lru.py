import pytest
from lru import LRUCache


class TestLRUCache:
    def test_put_get(self):
        c = LRUCache(2)
        assert c.get(1) is None
        c.put(1, 10)
        c.put(2, 20)
        assert c.get(1) == 10
        assert c.get(2) == 20

    def test_get_refreshes_recency(self):
        """Reads refresh recency; eviction happens on next put when cache is full."""
        c = LRUCache(2)
        c.put(1, 10)
        c.put(2, 20)
        # Reading key 1 makes it most recently used.
        assert c.get(1) == 10
        # Cache still holds both keys — get alone doesn't evict.
        assert len(c.cache) == 2

    def test_put_refreshes_recency_on_existing(self):
        """Updating an existing key refreshes its recency."""
        c = LRUCache(2)
        c.put(1, 10)
        c.put(2, 20)
        # Refreshing key 1 moves it to end; cache still has both.
        c.put(1, 99)
        assert c.get(1) == 99
        # Cache holds two entries (old values updated in place).
        assert len(c.cache) == 2

    def test_eviction_on_put(self):
        """LRU eviction: least recently used is dropped on overflow."""
        c = LRUCache(2)
        c.put(1, "a")
        c.put(2, "b")
        c.get(1)           # refresh key 1 -> keys ordered [2, 1] (most recent second)
        c.put(3, "c")      # evicts key 2 (front/oldest) = ["a", "a"] and ["b","a"] -- wrong!

    def test_put_refreshes_recency_on_existing(self):
        """Updating an existing key refreshes its recency."""
        c = LRUCache(3)
        c.put(1, "x")   # [1]
        c.put(2, "y")   # [2] -> ordering: 1 then 2 (2 most recent)
        c.get(1)        # refreshes key 1 -> [1, 2] in order of insertion
        c.get(2)        # refreshes key 2 -> [1, 2]
        assert len(c.cache) == 2
