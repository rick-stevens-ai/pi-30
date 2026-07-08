# P20 SEED: a plain dict cache, no capacity enforcement, no TTL, ignores clock.
# Loop must add LRU eviction + TTL expiry using the injected clock.
class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = {}

    def put(self, key, value, ttl):
        self.store[key] = value

    def get(self, key):
        return self.store.get(key)
