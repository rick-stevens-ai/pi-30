from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = OrderedDict()

    def put(self, key, value, ttl):
        if key in self.store:
            del self.store[key]
        elif len(self.store) >= self.capacity:
            # Evict LRU (the first item in OrderedDict)
            self.store.popitem(last=False)
        
        expiry = self.clock() + ttl
        self.store[key] = (value, expiry)

    def get(self, key):
        if key not in self.store:
            return None
        
        value, expiry = self.store[key]
        if self.clock() >= expiry:
            del self.store[key]
            return None
        
        # Move to end (MRU)
        self.store.move_to_end(key)
        return value
