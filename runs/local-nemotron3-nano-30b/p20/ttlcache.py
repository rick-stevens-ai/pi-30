# P20 SEED: LRU cache with per-entry TTL expiry using injected clock.
import collections

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        # OrderedDict maintains insertion order; we use it to track recency.
        self.store = collections.OrderedDict()

    def _remove_expired(self):
        """Delete entries whose expiration time is <= current clock time."""
        now = self.clock()
        expired_keys = [k for k, (_, expire) in self.store.items() if expire <= now]
        for k in expired_keys:
            del self.store[k]

    def put(self, key, value, ttl):
        # If the key already exists, remove it to reset its recency.
        if key in self.store:
            del self.store[key]

        # Remove any expired entries before considering capacity.
        self._remove_expired()

        # Ensure we have room for a new entry by evicting LRU items if needed.
        while len(self.store) >= self.capacity:
            self.store.popitem(last=False)  # remove least recently used item

        expire = self.clock() + ttl
        self.store[key] = (value, expire)

    def get(self, key):
        now = self.clock()
        if key not in self.store:
            return None

        value, expire = self.store[key]
        # If expired, remove it and treat as a miss.
        if now >= expire:
            del self.store[key]
            return None
        # Move the accessed entry to the end to mark it as most recently used.
        popped = self.store.pop(key)
        self.store[key] = popped
        return value