
# P20 SEED: a plain dict cache, no capacity enforcement, no TTL, ignores clock.
# Loop must add LRU eviction + TTL expiry using the injected clock.
class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = {}  # key -> value
        self.access_times = {}  # key -> timestamp of last access (for LRU)

    def _now(self):
        return self.clock()

    def put(self, key, value, ttl):
        now = self._now()
        if key in self.store:
            # Refresh the TTL expiry for an existing key
            self.access_times[key] = now + ttl
        else:
            # Evict LRU entries until there's room (skip keys already being added)
            while len(self.store) >= self.capacity and key not in self.store:
                lru_key = min(self.access_times, key=lambda k: self.access_times[k])
                del self.store[lru_key]
                del self.access_times[lru_key]

            # Insert with expiry timestamp = now + ttl
            self.store[key] = value
            self.access_times[key] = now + ttl

    def get(self, key):
        if key not in self.store:
            return None

        now = self._now()
        # If expired, remove and treat as miss
        if now >= self.access_times[key]:
            del self.store[key]
            del self.access_times[key]
            return None

        # Update access time (move to MRU)
        self.access_times[key] = now
        return self.store[key]
