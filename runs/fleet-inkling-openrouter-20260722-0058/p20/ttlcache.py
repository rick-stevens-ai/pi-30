from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = OrderedDict()

    def put(self, key, value, ttl):
        now = self.clock()
        # Evict expired / LRU if needed before inserting when at capacity
        if key not in self.store and len(self.store) >= self.capacity:
            # Evict oldest until we have room; remove expired ones too
            # We just evict the oldest LRU entry(s)
            while len(self.store) >= self.capacity:
                oldest_key, (old_val, old_exp) = self.store.popitem(last=False)
        self.store[key] = (value, now + ttl)
        self.store.move_to_end(key)

    def get(self, key):
        now = self.clock()
        if key in self.store:
            value, exp = self.store[key]
            if now >= exp:
                # Expired
                del self.store[key]
                return None
            self.store.move_to_end(key)
            return value
        return None
