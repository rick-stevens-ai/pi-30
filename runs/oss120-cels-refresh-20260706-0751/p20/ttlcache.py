# P20 SEED: a plain dict cache, no capacity enforcement, no TTL, ignores clock.
# Loop must add LRU eviction + TTL expiry using the injected clock.
from collections import OrderedDict


class TTLCache:
    """LRU cache with per‑entry TTL.

    * ``capacity`` – maximum number of *non‑expired* entries to keep.
    * ``clock`` – a callable returning the current time (float).  This is
      injected so tests can control time deterministically.
    * ``put(key, value, ttl)`` stores ``value`` with a time‑to‑live of ``ttl``
      seconds.  The entry becomes the most‑recently‑used.
    * ``get(key)`` returns the stored value if the entry exists **and** has not
      expired; otherwise ``None``.  A successful ``get`` also marks the entry as
      most‑recently‑used.
    """

    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        # OrderedDict preserves insertion order; we move a key to the end on
        # access/insert to represent MRU status.
        # Mapping: key -> (value, expiry_timestamp)
        self.store = OrderedDict()

    # ---------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------
    def _now(self):
        """Return the current time using the injected clock."""
        return self.clock()

    def _is_expired(self, expiry):
        return expiry <= self._now()

    def _purge_expired(self):
        """Remove all expired entries from the cache.

        Because ``OrderedDict`` stores items in LRU order, we can iterate over
        a copy of the keys and delete those whose expiry time has passed.
        """
        for key, (_, expiry) in list(self.store.items()):
            if self._is_expired(expiry):
                del self.store[key]

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def put(self, key, value, ttl):
        """Insert or update *key* with *value* that lives for *ttl* seconds.

        If the cache is at capacity, the least‑recently‑used non‑expired entry
        is evicted.  Expired entries are discarded first and do **not** count
        against capacity.
        """
        # Clean out any stale entries first.
        self._purge_expired()

        expiry = self._now() + ttl
        # If key already exists, replace its value/expiry and mark MRU.
        if key in self.store:
            del self.store[key]
            self.store[key] = (value, expiry)
            self.store.move_to_end(key)
            return

        # Ensure we have room for the new entry.
        while len(self.store) >= self.capacity:
            # popitem(last=False) removes the LRU entry.
            self.store.popitem(last=False)

        self.store[key] = (value, expiry)
        # New key is already at the end (MRU).

    def get(self, key):
        """Retrieve *key* if present and not expired; otherwise ``None``.

        A successful access updates the recency order.
        """
        if key not in self.store:
            return None
        value, expiry = self.store[key]
        if self._is_expired(expiry):
            # Remove the stale entry and report a miss.
            del self.store[key]
            return None
        # Refresh recency.
        self.store.move_to_end(key)
        return value
