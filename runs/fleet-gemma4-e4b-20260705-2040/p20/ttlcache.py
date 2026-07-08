from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        # store maps key -> (value, expiry_time)
        self.store = OrderedDict()

    def put(self, key, value, ttl):
        expiry_time = self.clock() + ttl
        if key in self.store:
            del self.store[key]  # Update existing entry to refresh TTL/LRU
        
        self.store[key] = (value, expiry_time)
        
        # Enforce capacity and LRU eviction
        if len(self.store) > self.capacity:
            # Pop the first item (Least Recently Used)
            self.store.popitem(last=False)

    def get(self, key):
        if key not in self.store:
            return None

        value, expiry_time = self.store[key]
        current_time = self.clock()

        # Check TTL expiry
        if current_time >= expiry_time:
            # Entry is expired, treat as a miss and evict it
            del self.store[key]
            return None
        
        # Valid entry: update LRU status (move to end)
        self.store.move_to_end(key)
        return value
