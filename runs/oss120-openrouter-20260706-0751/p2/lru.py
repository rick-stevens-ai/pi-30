"""Simple LRU Cache implementation with O(1) operations.

Provides a class `LRUCache` with methods:
- `get(key)`: Return the value associated with `key` or ``None`` if not present.
- `put(key, value)`: Insert or update the key with the given value. If the cache exceeds its capacity,
  the least‑recently used item is evicted.

Both ``get`` and ``put`` count as usage, i.e. they move the accessed/updated key to the most‑recent position.

Implementation uses a doubly‑linked list for the usage order and a dict for fast lookup.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.prev: Optional["_Node"] = None
        self.next: Optional["_Node"] = None


class LRUCache:
    """Least‑Recently Used cache with O(1) ``get`` and ``put``.

    Parameters
    ----------
    capacity: int
        Maximum number of items the cache can hold. Must be positive.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self.capacity = capacity
        self._map: Dict[Any, _Node] = {}
        # Dummy head and tail to avoid edge‑case checks
        self._head = _Node(None, None)  # Most‑recently used follows head
        self._tail = _Node(None, None)  # Least‑recently used precedes tail
        self._head.next = self._tail
        self._tail.prev = self._head

    # ---------------------------------------------------------------------
    # Internal helpers for list manipulation
    # ---------------------------------------------------------------------
    def _remove(self, node: _Node) -> None:
        """Unlink *node* from the doubly linked list."""
        prev, nxt = node.prev, node.next
        if prev is not None:
            prev.next = nxt
        if nxt is not None:
            nxt.prev = prev
        node.prev = node.next = None

    def _add_to_front(self, node: _Node) -> None:
        """Insert *node* right after the dummy head (most recent position)."""
        first = self._head.next
        self._head.next = node
        node.prev = self._head
        node.next = first
        if first is not None:
            first.prev = node

    def _move_to_front(self, node: _Node) -> None:
        """Move an existing *node* to the most‑recent position."""
        self._remove(node)
        self._add_to_front(node)

    def _evict_if_needed(self) -> None:
        """Evict the least‑recently used item when over capacity."""
        if len(self._map) > self.capacity:
            # The node before the dummy tail is the LRU entry
            lru = self._tail.prev
            if lru is None or lru is self._head:
                return  # Should not happen
            self._remove(lru)
            del self._map[lru.key]

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def get(self, key: Any) -> Any:
        """Return the value for *key* or ``None`` if the key is missing.

        Access counts as usage, moving the key to the most‑recent position.
        """
        node = self._map.get(key)
        if node is None:
            return None
        self._move_to_front(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """Insert or update *key* with *value*.

        If the key already exists its value is replaced and it becomes the most
        recently used entry. When the cache exceeds its capacity the least
        recently used entry is evicted.
        """
        if key in self._map:
            node = self._map[key]
            node.value = value
            self._move_to_front(node)
        else:
            node = _Node(key, value)
            self._map[key] = node
            self._add_to_front(node)
            self._evict_if_needed()

    # For debugging / testing convenience
    def _keys_mru_to_lru(self) -> list:
        """Return a list of keys from most‑recent to least‑recent.
        Not part of the public API; used in tests.
        """
        keys = []
        cur = self._head.next
        while cur and cur is not self._tail:
            keys.append(cur.key)
            cur = cur.next
        return keys
