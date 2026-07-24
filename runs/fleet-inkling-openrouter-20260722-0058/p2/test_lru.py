import pytest
from lru import LRUCache

def test_basic_get_put():
    c = LRUCache(2)
    c.put(1, 1)
    assert c.get(1) == 1
    assert c.get(2) is None

def test_eviction():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(3, 3)  # evicts 1
    assert c.get(1) is None
    assert c.get(2) == 2
    assert c.get(3) == 3

def test_get_refreshes():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1  # refresh 1
    c.put(3, 3)  # evicts 2
    assert c.get(2) is None
    assert c.get(1) == 1

def test_put_existing_updates_and_refreshes():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)
    c.put("c", 3)  # evicts b
    assert c.get("b") is None
    assert c.get("a") == 10
    assert c.get("c") == 3

def test_capacity_one():
    c = LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) is None
    assert c.get(2) == 2

def test_put_on_existing_updates_value():
    c = LRUCache(3)
    c.put(1, 1)
    c.put(1, 100)
    assert c.get(1) == 100

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
