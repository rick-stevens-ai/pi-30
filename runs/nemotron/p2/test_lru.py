import pytest
from lru import LRUCache


class TestLRUCache:
    def test_basic_put_get(self):
        c = LRUCache(2)
        c.put(1, 1)
        c.put(2, 2)
        assert c.get(1) == 1
        assert c.get(2) == 2

    def test_get_nonexistent_returns_none(self):
        c = LRUCache(2)
        assert c.get(1) is None
        assert c.get("nonexistent") is None

    def test_eviction_order(self):
        c = LRUCache(2)
        c.put(1, 1)
        c.put(2, 2)
        c.get(1)          # 1 is MRU, 2 is LRU
        c.put(3, 3)       # evicts 2
        assert c.get(2) is None
        assert c.get(1) == 1
        assert c.get(3) == 3

    def test_get_updates_recency(self):
        c = LRUCache(3)
        c.put(1, 1)
        c.put(2, 2)
        c.put(3, 3)
        c.get(1)          # 1 is MRU, order: 1, 3, 2
        c.get(3)          # 3 is MRU, order: 3, 1, 2
        c.put(4, 4)       # evicts 2
        assert c.get(2) is None
        assert c.get(1) == 1
        assert c.get(3) == 3
        assert c.get(4) == 4

    def test_put_existing_key_updates_value_and_recency(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("a", 10)    # update "a", makes it MRU
        c.put("c", 3)     # evicts "b"
        assert c.get("b") is None
        assert c.get("a") == 10
        assert c.get("c") == 3

    def test_capacity_one(self):
        c = LRUCache(1)
        c.put(1, 1)
        assert c.get(1) == 1
        c.put(2, 2)       # evicts 1
        assert c.get(1) is None
        assert c.get(2) == 2
        c.put(2, 20)      # update existing
        assert c.get(2) == 20

    def test_capacity_three_eviction_order(self):
        c = LRUCache(3)
        c.put(1, 1)
        c.put(2, 2)
        c.put(3, 3)
        c.get(1)          # 1 MRU, order: 1, 3, 2
        c.get(3)          # 3 MRU, order: 3, 1, 2
        c.put(4, 4)       # evicts 2
        assert c.get(2) is None
        c.put(5, 5)       # evicts 1 (order: 5, 4, 3)
        assert c.get(1) is None
        assert c.get(3) == 3
        assert c.get(4) == 4
        assert c.get(5) == 5

    def test_get_updates_recency_changes_eviction(self):
        c = LRUCache(2)
        c.put("x", 1)
        c.put("y", 2)
        assert c.get("x") == 1  # x is now MRU
        c.put("z", 3)           # evicts y
        assert c.get("y") is None
        assert c.get("x") == 1
        assert c.get("z") == 3

    def test_update_key_refreshes_recency(self):
        c = LRUCache(2)
        c.put(1, 1)
        c.put(2, 2)
        c.put(1, 10)      # update 1, makes it MRU
        c.put(3, 3)       # evicts 2
        assert c.get(2) is None
        assert c.get(1) == 10
        assert c.get(3) == 3

    def test_capacity_two_alternating(self):
        c = LRUCache(2)
        c.put(1, 1)
        c.put(2, 2)
        c.get(1)
        c.put(3, 3)       # evicts 2
        assert c.get(2) is None
        c.get(3)
        c.put(4, 4)       # evicts 1
        assert c.get(1) is None
        assert c.get(3) == 3
        assert c.get(4) == 4

    def test_string_keys(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        assert c.get("a") == 1
        assert c.get("b") == 2
        c.put("c", 3)     # evicts "a"
        assert c.get("a") is None
        assert c.get("b") == 2
        assert c.get("c") == 3

    def test_none_value(self):
        c = LRUCache(2)
        c.put(1, None)
        assert c.get(1) is None  # value is None, but key exists
        c.put(2, 2)
        c.put(3, 3)              # evicts 1
        assert c.get(1) is None  # key 1 evicted
        assert c.get(2) == 2

    def test_zero_capacity_raises(self):
        with pytest.raises(ValueError):
            LRUCache(0)

    def test_negative_capacity_raises(self):
        with pytest.raises(ValueError):
            LRUCache(-1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])