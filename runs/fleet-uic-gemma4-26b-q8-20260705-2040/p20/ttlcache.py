from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = OrderedDict()

    def put(self, key, value, ttl):
        expiry_time = self.clock() + ttl
        if key in self.store:
            self.store[key] = (value, expiry_time)
            self.store.move_to_end(key)
        else:
            if len(self.store) >= self.capacity:
                self.store.popitem(last=False)
            self.store[key] = (value, expiry_time)

    def get(self, key):
        if key not in self.store:
            return None
        
        value, expiry_time = self.store[key]
        if expiry_time <= self.clock():
            del self.store[key]
            return None
        
        self.store.move_to_end(key)
        return value
