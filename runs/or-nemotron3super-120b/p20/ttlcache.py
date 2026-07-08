# P20 SEED: a plain dict cache, no capacity enforcement, no TTL, ignores clock.
# Loop must add LRU eviction + TTL expiry using the injected clock.
class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = {}  # key -> (value, expiry_time)

    def put(self, key, value, ttl):
        # If key exists, update value and expiry, and move to end (most recently used)
        if key in self.store:
            expiry = self.clock() + ttl
            self.store[key] = (value, expiry)
            # Move to end by reinserting
            val_ex = self.store.pop(key)
            self.store[key] = val_ex
            return

        # Key does not exist: first remove expired entries
        now = self.clock()
        expired_keys = [k for k, (_, exp) in self.store.items() if exp <= now]
        for k in expired_keys:
            del self.store[k]

        # If still at or over capacity, remove LRU items (front of dict) until under capacity
        while len(self.store) >= self.capacity:
            if self.store:
                first_key = next(iter(self.store))
                del self.store[first_key]
            else:
                break

        # Insert new key-value pair
        expiry = self.clock() + ttl
        self.store[key] = (value, expiry)

    def get(self, key):
        if key not in self.store:
            return None
        value, expiry = self.store[key]
        now = self.clock()
        if expiry <= now:
            # Expired: remove it and return None
            del self.store[key]
            return None
        # Not expired: move to end (most recently used) and return value
        self.store.pop(key)
        self.store[key] = (value, expiry)
        return value