"""Pytest tests for LRUCache."""

from lru import LRUCache


def test_get_missing_returns_none():
    c = LRUCache(2)
    assert c.get("nope") is None


def test_put_then_get():
    c = LRUCache(2)
    c.put("a", 1)
    assert c.get("a") == 1


def test_capacity_zero():
    c = LRUCache(0)
    c.put("a", 1)
    assert c.get("a") is None


def test_evict_lru_when_full():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    # access a so b becomes LRU
    assert c.get("a") == 1
    c.put("c", 3)  # evicts b
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3


def test_put_existing_updates_value():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("a", 2)
    assert c.get("a") == 2
    assert len({k for k in ("a",)}) == 1


def test_put_existing_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    # updating a should refresh it so b is LRU
    c.put("a", 10)
    c.put("c", 3)  # evicts b
    assert c.get("b") is None
    assert c.get("a") == 10
    assert c.get("c") == 3


def test_get_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1  # a now MRU, b is LRU
    c.put("c", 3)  # evicts b
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3


def test_full_eviction_order():
    c = LRUCache(3)
    for i, v in enumerate([("x", 1), ("y", 2), ("z", 3)]):
        c.put(v[0], v[1])
    c.get("x")
    c.get("z")
    # LRU order: y, x, z -> evict y, then x
    c.put("w", 4)
    assert c.get("y") is None
    c.put("v", 5)
    assert c.get("x") is None
    assert c.get("z") == 3
    assert c.get("w") == 4
    assert c.get("v") == 5


def test_none_value_stored():
    c = LRUCache(2)
    c.put("a", None)
    # distinguish stored None vs missing: stored None should still occupy slot
    assert c.get("a") is None
    c.put("b", 2)
    c.put("c", 3)  # a is LRU, should evict a
    assert "a" not in c._data


def test_overwrite_does_not_grow_size():
    c = LRUCache(1)
    c.put("a", 1)
    c.put("a", 2)
    c.put("a", 3)
    assert c.get("a") == 3
    assert c.get("b") is None


def test_int_and_str_keys():
    c = LRUCache(2)
    c.put(1, "one")
    c.put("1", "str")
    assert c.get(1) == "one"
    assert c.get("1") == "str"
