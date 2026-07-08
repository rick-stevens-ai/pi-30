import pytest
from lru import LRUCache

def test_basic_put_get():
    c = LRUCache(2)
    c.put(1, 'a')
    c.put(2, 'b')
    assert c.get(1) == 'a'
    # after get(1), order is 1 (MRU),2
    c.put(3, 'c')  # should evict key 2
    assert c.get(2) is None
    assert c.get(1) == 'a'
    assert c.get(3) == 'c'

def test_update_refreshes():
    c = LRUCache(2)
    c.put('x', 1)
    c.put('y', 2)
    # update x, should become MRU
    c.put('x', 10)
    c.put('z', 3)  # evicts y
    assert c.get('y') is None
    assert c.get('x') == 10
    assert c.get('z') == 3

def test_get_counts_as_use():
    c = LRUCache(2)
    c.put('a', 1)
    c.put('b', 2)
    c.get('a')  # a becomes MRU
    c.put('c', 3)  # evicts b
    assert c.get('b') is None
    assert c.get('a') == 1
    assert c.get('c') == 3

def test_capacity_one():
    c = LRUCache(1)
    c.put(1, 'first')
    assert c.get(1) == 'first'
    c.put(2, 'second')
    assert c.get(1) is None
    assert c.get(2) == 'second'

def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)

def test_internal_order():
    c = LRUCache(3)
    c.put(1, 'a')
    c.put(2, 'b')
    c.put(3, 'c')
    assert c._keys_mru_to_lru() == [3,2,1]
    c.get(1)
    assert c._keys_mru_to_lru() == [1,3,2]
    c.put(4, 'd')
    # should evict 2
    assert c._keys_mru_to_lru() == [4,1,3]
