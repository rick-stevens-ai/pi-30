import pytest
from lru import LRUCache


class TestBasicOps:
    def test_put_and_get(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        assert cache.get(1) == 10

    def test_miss_returns_none(self):
        cache = LRUCache(2)
        assert cache.get(99) is None


class TestEviction:
    def test_evicts_lru(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        # Accessing key=1 makes it most recent; key=2 is LRU
        assert cache.get(1) == 10
        cache.put(3, 30)  # Should evict key=2
        assert cache.get(2) is None
        assert cache.get(1) == 10
        assert cache.get(3) == 30

    def test_evicts_first_inserted_when_no_access(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        cache.put(3, 30)  # Should evict key=1 (LRU)
        assert cache.get(1) is None
        assert cache.get(2) == 20
        assert cache.get(3) == 30

    def test_put_updates_existing_key(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(1, 99)
        assert cache.get(1) == 99


class TestGetRefreshesRecency:
    def test_get_makes_recent(self):
        cache = LRUCache(3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        # key=1 is LRU; accessing it refreshes recency
        assert cache.get(1) == 1
        cache.put(4, 4)  # Should evict key=2 (now LRU)
        assert cache.get(2) is None
        assert cache.get(1) == 1
        assert cache.get(3) == 3
        assert cache.get(4) == 4


class TestPutRefreshesRecency:
    def test_put_refreshes_existing_key(self):
        cache = LRUCache(3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        # Touching key=1 should push it to most recent
        cache.put(1, 10)
        cache.put(4, 4)  # Should evict key=2 (now LRU)
        assert cache.get(2) is None
        assert cache.get(1) == 10
        assert cache.get(3) == 3
        assert cache.get(4) == 4


class TestCapacityOne:
    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put(1, 10)
        assert cache.get(1) == 10
        cache.put(2, 20)  # Evicts key=1
        assert cache.get(1) is None
        assert cache.get(2) == 20


class TestEdgeCases:
    def test_put_same_value(self):
        cache = LRUCache(2)
        cache.put(1, 5)
        cache.put(1, 5)
        assert cache.get(1) == 5

    def test_zero_capacity_rejected(self):
        with pytest.raises(ValueError, match="capacity must be >= 1"):
            LRUCache(0)

    def test_negative_capacity_rejected(self):
        with pytest.raises(ValueError, match="capacity must be >= 1"):
            LRUCache(-5)

    def test_multiple_put_get_cycle(self):
        cache = LRUCache(4)
        for i in range(10):
            cache.put(i, i * 10)
        # Only last 4 keys remain: 6,7,8,9
        assert cache.get(5) is None
        assert cache.get(6) == 60
        assert cache.get(7) == 70
        assert cache.get(8) == 80
        assert cache.get(9) == 90

    def test_get_on_filled_cache_preserves_order(self):
        cache = LRUCache(3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(3, "c")
        # Touch key=1: order becomes [1, 2, 3] => most recent first => recency=[1,3,2]
        assert cache.get(1) == "a"
        # Now LRU is key=2
        cache.put(4, "d")
        assert cache.get(2) is None

    def test_put_updates_value_and_counts_as_use(self):
        """Putting on an existing key should update the value AND refresh recency."""
        cache = LRUCache(3)
        cache.put(10, 100)
        cache.put(20, 200)
        cache.put(30, 300)

        # Touch key=10 so it's recent: recency ~ [10, 30, 20]
        assert cache.get(10) == 100

        # Update key=20 via put => refreshes it to most recent: recency ~ [20(new), 10, 30]
        cache.put(20, 999)

        # Now LRU is key=30, so it gets evicted next
        cache.put(40, 400)

        assert cache.get(30) is None
        assert cache.get(10) == 100
        assert cache.get(20) == 999
        assert cache.get(40) == 400


class TestO1Complexity:
    def test_operations_are_fast(self):
        """Rudimentary check that operations are O(1) — no timeout."""
        import time
        cache = LRUCache(10_000)

        # Fill it up
        for i in range(10_000):
            cache.put(i, i)

        start = time.monotonic()
        # Random get/put — should not be noticeably slow
        for _ in range(5_000):
            key = 7 * (_ * 3 + 1) % 9_999
            cache.get(key)
            cache.put(key, key + 1000)
        elapsed = time.monotonic() - start
        assert elapsed < 2.0  # generous timeout
