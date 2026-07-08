"""LRU Cache implementation with O(1) get and put operations.

The cache stores a fixed number of key/value pairs defined by ``capacity``.
When the cache exceeds this capacity the least‑recently‑used entry is evicted.
Both ``get`` and ``put`` count as usage: accessing an entry moves it to the
most‑recent position and inserting a new key (or updating an existing one)
also refreshes its recency.

Only the Python standard library is used – the implementation relies on
``collections.OrderedDict`` which provides ``move_to_end`` and ``popitem`` in
amortised O(1) time.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    """Least‑Recently‑Used (LRU) cache.

    Parameters
    ----------
    capacity: int
        Maximum number of items the cache can hold. ``capacity`` must be a
        positive integer; a ``ValueError`` is raised otherwise.

    Methods
    -------
    get(key) -> Optional[Any]
        Return the value associated with *key* if present, otherwise ``None``.
        The accessed item becomes the most‑recently used.
    put(key, value) -> None
        Insert or update *key* with *value*. If the cache would exceed its
        capacity the least‑recently used entry is evicted.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self._capacity = capacity
        # OrderedDict preserves insertion order; the *right* end is the most recent.
        self._store: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        """Return the value for *key* and mark it as recently used.

        If *key* is not present ``None`` is returned.
        """
        if key not in self._store:
            return None
        # Move the key to the end to denote recent use
        self._store.move_to_end(key, last=True)
        return self._store[key]

    def put(self, key: Any, value: Any) -> None:
        """Insert *key* with *value* (or update existing) and mark as recent.
        Evicts the least‑recently used item if the capacity would be exceeded.
        """
        if key in self._store:
            # Update value and refresh recency
            self._store[key] = value
            self._store.move_to_end(key, last=True)
        else:
            self._store[key] = value
            # If we just exceeded capacity, pop the LRU item (the first one)
            if len(self._store) > self._capacity:
                self._store.popitem(last=False)

    # Helper methods for debugging / tests (not required by the task but handy)
    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key: Any) -> bool:
        return key in self._store

    def __repr__(self) -> str:
        return f"LRUCache(capacity={self._capacity}, items={list(self._store.items())})"
