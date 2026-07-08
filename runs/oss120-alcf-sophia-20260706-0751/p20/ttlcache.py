# TTLCache implementation with LRU eviction and per‑entry TTL expiry.
# Uses an injected ``clock`` (callable returning current time) for deterministic testing.
# The cache stores entries as (value, expiry_time) and maintains LRU order via ``OrderedDict``.
# Expired entries are treated as misses and removed, and they do not count against capacity.

from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        """Create a cache with a maximum *capacity* and a *clock* callable.
        ``clock()`` should return the current time as a float.
        """
        self.capacity = capacity
        self.clock = clock
        # OrderedDict preserves insertion order; we treat the end as MRU.
        self.store = OrderedDict()

    def _purge_expired(self):
        """Remove all entries whose expiry time is <= current time.
        This is called before any operation that may need free space.
        """
        now = self.clock()
        # Collect keys to delete to avoid modifying dict during iteration.
        expired_keys = [k for k, (_, exp) in self.store.items() if exp <= now]
        for k in expired_keys:
            del self.store[k]

    def put(self, key, value, ttl):
        """Insert or update *key* with *value* that lives for *ttl* seconds.
        If the cache is at capacity, the least‑recently‑used (LRU) non‑expired
        entry is evicted. Expired entries are discarded first and do not count
        toward capacity.
        """
        now = self.clock()
        expiry = now + ttl
        # Remove any stale entries first.
        self._purge_expired()

        if key in self.store:
            # Update existing entry and move it to MRU position.
            self.store[key] = (value, expiry)
            self.store.move_to_end(key)
            return

        # Ensure there is space for the new entry.
        while len(self.store) >= self.capacity:
            # Peek at the LRU entry (first item).
            lru_key, (_, lru_exp) = next(iter(self.store.items()))
            if lru_exp <= now:
                # LRU is already expired; purge it and continue.
                del self.store[lru_key]
                continue
            # Evict the LRU entry.
            del self.store[lru_key]
            break

        # Insert the new entry as MRU.
        self.store[key] = (value, expiry)

    def get(self, key):
        """Retrieve the value for *key* if present and not expired.
        Returns ``None`` for a miss or an expired entry (which is also removed).
        Accessing a valid entry marks it as most‑recently‑used.
        """
        now = self.clock()
        entry = self.store.get(key)
        if entry is None:
            return None
        value, expiry = entry
        if expiry <= now:
            # Expired – remove and report miss.
            del self.store[key]
            return None
        # Refresh LRU order: move to end (MRU).
        self.store.move_to_end(key)
        return value

