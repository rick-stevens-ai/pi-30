import collections


class TTLCache:
    def __init__(self, capacity, ttl=None, clock=None):
        self.capacity = capacity
        self.default_ttl = ttl
        self.clock = clock
        # OrderedDict maps key -> (value, expiry_time), front = LRU.
        self.store = collections.OrderedDict()

    def get(self, key):
        if key not in self.store:
            return None
        value, expiry = self.store[key]
        now = self.clock()
        if now >= expiry:
            # Expired: treat as a miss and drop the entry so it no longer
            # counts against capacity.
            del self.store[key]
            return None
        # Mark as most-recently-used.
        self.store.move_to_end(key)
        return value

    def put(self, key, value, ttl):
        # Re-inserting an existing key moves it to MRU position.
        if key in self.store:
            del self.store[key]
        self.store[key] = (value, self.clock() + ttl)
        # Enforce capacity via LRU eviction (front of the OrderedDict).
        while len(self.store) > self.capacity:
            self.store.popitem(last=False)