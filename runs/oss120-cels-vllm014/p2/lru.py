"""lr u cache implementation with O(1) get and put.

The cache stores at most *capacity* items.  Access via ``get`` or ``put``
marks the key as most‑recently used.  When the capacity would be exceeded the
least‑recently used entry is evicted.

Only the Python standard library is used – ``collections.OrderedDict`` gives
the required O(1) ordered‑dictionary semantics.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Optional

__all__ = ["LRUCache"]


class LRUCache:
    """A fixed‑size LRU (least‑recently used) cache.

    Parameters
    ----------
    capacity: int
        Maximum number of entries the cache can hold.  ``capacity`` must be a
        positive integer; a ``ValueError`` is raised otherwise.

    Methods
    -------
    get(key) -> Any | None
        Return the cached value associated with *key*, or ``None`` if the key
        is not present.  Access counts as a use and moves the key to the most
        recent position.
    put(key, value) -> None
        Insert *value* under *key*.  If *key* already exists its value is
        replaced and it is refreshed as most‑recent.  When the cache is full a
        least‑recently used entry is evicted.
    """

    def __init__(self, capacity: int):
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self._capacity: int = capacity
        # OrderedDict preserves insertion order.  The *right* side holds the
        # most‑recently used entry; the *left* side holds the least‑recently
        # used entry.
        self._data: OrderedDict[Any, Any] = OrderedDict()

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def get(self, key: Any) -> Optional[Any]:
        """Return the value for *key* if present, else ``None``.

        When the key exists it is moved to the most‑recent position because a
        lookup counts as a use.
        """
        if key not in self._data:
            return None
        # ``pop`` + re‑insert moves the entry to the right end in O(1).
        value = self._data.pop(key)
        self._data[key] = value
        return value

    def put(self, key: Any, value: Any) -> None:
        """Insert or update *key* with *value*.

        Updating an existing key also refreshes its recency.  If the cache is
        at capacity and the key is new, the least‑recently used entry is evicted
        before insertion.
        """
        if key in self._data:
            # Remove the old entry first – ``pop`` followed by insert moves it
            # to the most‑recent position.
            self._data.pop(key)
        elif len(self._data) >= self._capacity:
            # Evict the least‑recently used (left‑most) entry.
            self._data.popitem(last=False)
        self._data[key] = value

    # ---------------------------------------------------------------------
    # Helper methods (useful for debugging / introspection, not required by the
    # specification but harmless).
    # ---------------------------------------------------------------------
    def __len__(self) -> int:  # pragma: no cover – trivial
        return len(self._data)

    def __repr__(self) -> str:  # pragma: no cover – debugging aid
        return f"LRUCache(capacity={self._capacity}, items={list(self._data.items())})"
