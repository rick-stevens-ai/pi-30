"""O(1) LRU cache using a doubly linked list + dict.

get and put both count as use. put on an existing key updates the value
and refreshes recency. When capacity is exceeded, the least recently
used item is evicted.
"""

from __future__ import annotations


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev: "_Node | None" = None
        self.next: "_Node | None" = None


class LRUCache:
    """Least-recently-used cache with O(1) get/put."""

    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self.capacity = capacity
        self._cache: dict = {}
        # Sentinel head/tail bound the list.
        # Most-recently-used sits right after head; least-recently-used
        # sits right before tail.
        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    # -- linked list helpers (assume node is in list) ---------------------

    def _remove(self, node: _Node) -> None:
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node  # type: ignore[union-attr]
        next_node.prev = prev_node  # type: ignore[union-attr]

    def _add_front(self, node: _Node) -> None:
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node  # type: ignore[union-attr]
        self._head.next = node

    def _move_to_front(self, node: _Node) -> None:
        self._remove(node)
        self._add_front(node)

    def _pop_lru(self) -> _Node:
        """Remove and return the least-recently-used node (before tail)."""
        lru = self._tail.prev
        self._remove(lru)  # type: ignore[arg-type]
        return lru  # type: ignore[return-value]

    # -- public API -------------------------------------------------------

    def get(self, key):
        """Return value for key, or None if absent. Counts as a use."""
        node = self._cache.get(key)
        if node is None:
            return None
        self._move_to_front(node)
        return node.value

    def put(self, key, value) -> None:
        """Insert or update key/value, refreshing recency. Evicts LRU if needed."""
        if self.capacity == 0:
            return
        node = self._cache.get(key)
        if node is not None:
            node.value = value
            self._move_to_front(node)
            return
        node = _Node(key, value)
        self._cache[key] = node
        self._add_front(node)
        if len(self._cache) > self.capacity:
            lru = self._pop_lru()
            del self._cache[lru.key]

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, key) -> bool:
        return key in self._cache

    def __repr__(self) -> str:
        return f"LRUCache(capacity={self.capacity}, size={len(self)})"