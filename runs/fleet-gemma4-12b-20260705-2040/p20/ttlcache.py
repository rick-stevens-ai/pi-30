from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = OrderedDict()

    def put(self, key, value, ttl):
        expiry_time = self.clock() + ttl
        if key in self.store:
            # Update existing entry and move to end (MRU)
            self.store[key] = (value, expiry_time)
            self.store.move_to_end(key)
        else:
            if len(self.store) >= self.capacity:
                # Evict LRU (first item)
                self.store.popitem(last=False)
            self.store[key] = (value, expiry_time)

    def get(self, key):
        if key not in self.store:
            return None
        
        val, expiry = self.store[key]
        now = self.clock()
        
        if now >= expiry:
            # Remove expired entry
            del self.store[key]
            return None
        else:
            # Move to end (MRU)
            self.store.move_to_end(key)
            return val
