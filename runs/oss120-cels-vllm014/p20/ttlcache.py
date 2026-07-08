# TTLCache implementation with capacity, per-entry TTL, and LRU eviction.
# Uses an injected clock callable for deterministic time handling.
# Stores entries in an OrderedDict to track recency (MRU at the end).
# Expired entries are treated as misses and removed, and do not count against capacity.
from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity            # Maximum number of non‑expired entries
        self.clock = clock                  # Callable returning current time
        self.store = OrderedDict()          # key -> (value, expiry_time)

    def _is_expired(self, expiry):
        """Return True if the given expiry time is in the past."""
        return self.clock() > expiry

    def _purge_expired(self):
        """Remove all expired items from the cache.
        Called before capacity checks to ensure only live entries count.
        """
        now = self.clock()
        # Collect keys to delete to avoid mutating during iteration
        expired_keys = [k for k, (_, exp) in self.store.items() if now > exp]
        for k in expired_keys:
            del self.store[k]

    def put(self, key, value, ttl):
        """Insert or update *key* with *value* that lives for *ttl* seconds.
        Moves the key to the MRU position. If capacity is exceeded, evicts the
        LRU non‑expired entry.
        """
        expiry = self.clock() + ttl
        # If key exists, simply replace value and expiry, and mark MRU
        if key in self.store:
            self.store[key] = (value, expiry)
            self.store.move_to_end(key)
            return

        # Clean out any stale entries before possibly evicting
        self._purge_expired()

        # Evict LRU entries until we have room for the new one
        while len(self.store) >= self.capacity:
            # popitem(last=False) removes the oldest (LRU) entry
            evicted_key, _ = self.store.popitem(last=False)
            # If the evicted entry was expired, continue popping (capacity still full)
            # but generally this loop will stop after removing a non‑expired LRU.
            # No further action needed.
            if len(self.store) < self.capacity:
                break

        # Insert the new entry as MRU
        self.store[key] = (value, expiry)
        # OrderedDict inserts at the end by default, representing MRU.

    def get(self, key):
        """Retrieve the value for *key* if present and not expired.
        Returns ``None`` on miss or expiry. Accessing a live entry marks it MRU.
        """
        entry = self.store.get(key)
        if entry is None:
            return None
        value, expiry = entry
        if self._is_expired(expiry):
            # Remove stale entry and report miss
            del self.store[key]
            return None
        # Refresh recency
        self.store.move_to_end(key)
        return value
