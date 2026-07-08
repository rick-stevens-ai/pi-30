"""Pytest suite for the LRUCache implementation.

The tests are straightforward reproductions of the behaviour verified
by `verify.py`, plus a few additional edge cases.
"""

from lru import LRUCache


def test_basic_eviction_and_reuse():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1  # access 1 makes 2 the LRU
    c.put(3, 3)  # should evict key 2
    assert c.get(2) is None
    c.put(4, 4)  # should evict key 1
    assert c.get(1) is None
    assert c.get(3) == 3
    assert c.get(4) == 4


def test_update_of_existing_key():
    c2 = LRUCache(2)
    c2.put("a", 1)
    c2.put("b", 2)
    c2.put("a", 10)  # update and make 'a' most recent
    c2.put("c", 3)  # should evict 'b'
    assert c2.get("b") is None
    assert c2.get("a") == 10
    assert c2.get("c") == 3


def test_capacity_one():
    c3 = LRUCache(1)
    c3.put(1, 1)
    c3.put(2, 2)  # evicts 1
    assert c3.get(1) is None
    assert c3.get(2) == 2


def test_eviction_order_with_access():
    c = LRUCache(3)
    c.put("x", "x1")
    c.put("y", "y1")
    c.put("z", "z1")
    # Access x to make it MRU
    assert c.get("x") == "x1"
    # now insert w, should evict y
    c.put("w", "w1")
    assert c.get("y") is None
    assert c.get("z") == "z1"
    assert c.get("w") == "w1"
    assert c.get("x") == "x1"


def test_zero_capacity():
    c = LRUCache(0)
    c.put("a", 1)
    assert c.get("a") is None  # never stored
    # no exception on put


def test_repr():
    c = LRUCache(2)
    c.put("k1", 1)
    c.put("k2", 2)
    repr_str = repr(c)
    assert "LRUCache" in repr_str
    assert "k1" in repr_str and "k2" in repr_str
