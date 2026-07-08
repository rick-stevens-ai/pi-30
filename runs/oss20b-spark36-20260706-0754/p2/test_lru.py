"""Pytest unit tests for :class:`LRUCache`.

The tests exercise basic cache semantics and the LRU eviction policy:

* ``get`` returns ``None`` when key missing.
* Inserting elements up to capacity keeps them all.
* Once capacity exceeded the least‑recently used item is evicted.
* ``put`` on an existing key updates its value and refreshes recency.
* The cache honours a capacity of zero (everything gets dropped).
"""

import pytest
from lru import LRUCache


def test_empty_cache():
    c = LRUCache(2)
    assert c.get("a") is None


def test_basic_put_get():
    c = LRUCache(2)
    c.put("x", 1)
    assert c.get("x") == 1
    assert c.get("y") is None


def test_eviction_order():
    c = LRUCache(2)
    c.put("a", 10)
    c.put("b", 20)
    # Access "a" to make it MRU
    assert c.get("a") == 10
    # Insert third element, "b" should be evicted as LRU
    c.put("c", 30)
    assert c.get("b") is None
    assert c.get("a") == 10
    assert c.get("c") == 30


def test_update_and_refresh():
    c = LRUCache(2)
    c.put("key", "first")
    # second put updates value and recency
    c.put("key", "second")
    assert c.get("key") == "second"
    # Cache should still hold the same single key
    assert len(c.cache) == 1


def test_capacity_zero():
    c = LRUCache(0)
    c.put("a", 1)
    assert c.get("a") is None
    assert len(c.cache) == 0


if __name__ == "__main__":
    pytest.main([__file__])
