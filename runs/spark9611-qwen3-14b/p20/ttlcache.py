# P20 SEED: a plain dict cache, no capacity enforcement, no TTL, ignores clock.
# Loop must add LRU eviction + TTL expiry using the injected clock.
from collections import OrderedDict
class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = OrderedDict()

self.store[key] = (value, self.clock())
        # Move to end of LRU list
        if key in self.store:
            del self.store[key]
        self.store[key] = (value, self.clock.time())

    def get(self, key):
        if key not in self.store:
            return None
        value, timestamp = self.store[key]
        if self.clock.time() - timestamp > ttl:
            del self.store[key]
            return None
        # Move to end of LRU list
        if key in self.store:
            del self.store[key]
        self.store[key] = (value, timestamp)
        return value
