# P20 SEED: a plain dict cache, no capacity enforcement, no TTL, ignores clock.
# Loop must add LRU eviction + TTL expiry using the injected clock.
class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = {}  # key -> (value, expiration_time)
        self.access_order = []  # maintain LRU order

    def put(self, key, value, ttl):
        current_time = self.clock()
        
        # Check if key exists and remove it from access_order if present
        if key in self.store:
            self.access_order.remove(key)
        else:
            # If cache is full, evict the least recently used item
            while len(self.store) >= self.capacity and self.access_order:
                lru_key = self.access_order.pop(0)
                if lru_key in self.store:
                    del self.store[lru_key]
        
        expiration_time = current_time + ttl
        self.store[key] = (value, expiration_time)
        self.access_order.append(key)

    def get(self, key):
        current_time = self.clock()
        
        if key not in self.store:
            return None
        
        value, expiration_time = self.store[key]
        
        # Check if expired
        if current_time > expiration_time:
            del self.store[key]
            if key in self.access_order:
                try:
                    self.access_order.remove(key)
                except ValueError:
                    pass
            return None
        
        # Update access order - move to end (most recently used)
        if key in self.access_order:
            try:
                self.access_order.remove(key)
            except ValueError:
                pass
            self.access_order.append(key)
        
        return value
