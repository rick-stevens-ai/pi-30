"""LRU Cache implementation using doubly linked list + hash map for O(1) get/put."""

class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """Least Recently Used (LRU) Cache with O(1) get and put operations.

    Args:
        capacity: Maximum number of key-value pairs to store. Must be >= 1.
    """

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._cache = {}  # key -> _Node

        # Dummy head and tail for simpler list operations
        self._head = _Node(None, None)  # most recently used (MRU)
        self._tail = _Node(None, None)  # least recently used (LRU)
        self._head.next = self._tail
        self._tail.prev = self._head

    def get(self, key):
        """Get value by key, marking it as recently used. Returns None if not found."""
        node = self._cache.get(key)
        if node is None:
            return None
        self._move_to_front(node)
        return node.value

    def put(self, key, value):
        """Insert or update key-value pair, marking as recently used.
        Evicts least recently used item if at capacity and key is new.
        """
        node = self._cache.get(key)
        if node is not None:
            # Update existing key - update value and move to front
            node.value = value
            self._move_to_front(node)
            return

        # New key - check capacity
        if len(self._cache) >= self._capacity:
            self._evict_lru()

        # Add new node
        node = _Node(key, value)
        self._cache[key] = node
        self._add_to_front(node)

    def _add_to_front(self, node):
        """Add node right after head (most recently used position)."""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _remove(self, node):
        """Remove node from linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_front(self, node):
        """Move existing node to front (most recently used)."""
        self._remove(node)
        self._add_to_front(node)

    def _evict_lru(self):
        """Remove least recently used node (before tail)."""
        lru = self._tail.prev
        self._remove(lru)
        del self._cache[lru.key]

    def __len__(self):
        return len(self._cache)

    def __contains__(self, key):
        return key in self._cache


# Bundled tests
if __name__ == "__main__":
    # Test 1: Basic LRU behavior from verifier
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1, "Test 1a: get(1) should return 1"
    c.put(3, 3)  # evicts 2
    assert c.get(2) is None, "Test 1b: get(2) should return None (evicted)"
    c.put(4, 4)  # evicts 1 (3 was just... 1 was used at get)
    assert c.get(1) is None, "Test 1c: get(1) should return None (evicted)"
    assert c.get(3) == 3, "Test 1d: get(3) should return 3"
    assert c.get(4) == 4, "Test 1e: get(4) should return 4"

    # Test 2: Update existing key counts as use and updates value
    c2 = LRUCache(2)
    c2.put("a", 1)
    c2.put("b", 2)
    c2.put("a", 10)  # a refreshed
    c2.put("c", 3)   # evicts b
    assert c2.get("b") is None, "Test 2a: get('b') should return None (evicted)"
    assert c2.get("a") == 10, "Test 2b: get('a') should return 10 (updated)"
    assert c2.get("c") == 3, "Test 2c: get('c') should return 3"

    # Test 3: Capacity 1 edge case
    c3 = LRUCache(1)
    c3.put(1, 1)
    c3.put(2, 2)
    assert c3.get(1) is None and c3.get(2) == 2, "Test 3: capacity 1 edge case"

    # Test 4: get returns None for missing keys
    c4 = LRUCache(2)
    assert c4.get("missing") is None, "Test 4a: get missing key returns None"
    c4.put("x", 1)
    assert c4.get("x") == 1, "Test 4b: get existing key returns value"

    # Test 5: Update existing key moves to MRU
    c5 = LRUCache(3)
    c5.put(1, 1)
    c5.put(2, 2)
    c5.put(3, 3)
    c5.get(1)  # 1 becomes MRU, order: 1, 3, 2 (LRU)
    c5.put(4, 4)  # evicts 2
    assert c5.get(2) is None, "Test 5a: 2 should be evicted"
    assert c5.get(1) == 1, "Test 5b: 1 should still exist"
    assert c5.get(3) == 3, "Test 5c: 3 should still exist"
    assert c5.get(4) == 4, "Test 5d: 4 should exist"

    # Test 6: Capacity validation
    try:
        LRUCache(0)
        assert False, "Test 6: Should raise ValueError for capacity 0"
    except ValueError:
        pass
    try:
        LRUCache(-1)
        assert False, "Test 6b: Should raise ValueError for negative capacity"
    except ValueError:
        pass

    # Test 7: __len__ and __contains__
    c7 = LRUCache(3)
    assert len(c7) == 0
    assert 1 not in c7
    c7.put(1, 1)
    assert len(c7) == 1
    assert 1 in c7
    c7.put(2, 2)
    assert len(c7) == 2
    assert 2 in c7
    c7.get(1)
    assert len(c7) == 2

    # Test 8: Eviction order correctness
    c8 = LRUCache(3)
    c8.put(1, 1)
    c8.put(2, 2)
    c8.put(3, 3)
    c8.get(1)      # 1 is MRU, order: 1, 3, 2
    c8.get(3)      # 3 is MRU, order: 3, 1, 2
    c8.put(4, 4)   # evicts 2
    assert c8.get(2) is None
    c8.put(5, 5)   # evicts 1 (order: 5, 4, 3)
    assert c8.get(1) is None
    assert c8.get(3) == 3
    assert c8.get(4) == 4
    assert c8.get(5) == 5

    # Test 9: get updates recency
    c9 = LRUCache(2)
    c9.put("x", 1)
    c9.put("y", 2)
    assert c9.get("x") == 1  # x is now MRU
    c9.put("z", 3)  # evicts y
    assert c9.get("y") is None
    assert c9.get("x") == 1
    assert c9.get("z") == 3

    # Test 10: Capacity 2, alternating updates
    c10 = LRUCache(2)
    c10.put(1, 1)
    c10.put(2, 2)
    c10.put(1, 10)  # update 1
    c10.put(3, 3)   # evicts 2
    assert c10.get(2) is None
    assert c10.get(1) == 10
    assert c10.get(3) == 3

    print("All bundled tests passed!")