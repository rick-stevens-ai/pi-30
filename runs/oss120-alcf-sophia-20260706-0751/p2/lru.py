import collections
from typing import Any, Optional


class LRUCache:
    """A simple LRU (Least Recently Used) cache.

    The cache stores up to ``capacity`` key/value pairs. ``get`` returns the value
    associated with ``key`` or ``None`` if the key is not present. Both ``get`` and
    ``put`` update the recency order: the accessed/updated key becomes the most
    recent. When the cache is full, adding a new key evicts the least‑recently
    used entry.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        # OrderedDict remembers insertion order; the *end* will be the most recent.
        self._data: collections.OrderedDict[Any, Any] = collections.OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        """Return the value for *key* if present, otherwise ``None``.

        The operation refreshes the key's recency so that it becomes the most
        recently used item.
        """
        if key not in self._data:
            return None
        # Move key to the end to mark it as recently used.
        value = self._data.pop(key)
        self._data[key] = value
        return value

    def put(self, key: Any, value: Any) -> None:
        """Insert ``key`` with ``value`` into the cache.

        If ``key`` already exists its value is updated and its recency is
        refreshed. If the cache is at full capacity a least‑recently used entry
        is evicted before the new item is stored.
        """
        if key in self._data:
            # Remove old entry so that the new one is placed at the end.
            self._data.pop(key)
        elif len(self._data) >= self.capacity:
            # popitem(last=False) removes the first (least‑recent) entry.
            self._data.popitem(last=False)
        self._data[key] = value

    # Optional convenience methods for debugging / representation
    def __repr__(self) -> str:
        return f"LRUCache(capacity={self.capacity}, data={list(self._data.items())})"
