# P20 SEED: a plain dict cache, no capacity enforcement, no TTL, ignores clock.
# Loop must add LRU eviction + TTL expiry using the injected clock.
class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = {}  # {key: (value, expiry_time)}
        self.access_order = []  # List to track access order for LRU

    def put(self, key, value, ttl):
        current_time = self.clock()
        expiry_time = current_time + ttl
        
        # If key exists, update it and move to end of access order
        if key in self.store:
            self.access_order.remove(key)
        else:
            # Check if we need to evict LRU item
            if len(self.store) >= self.capacity:
                # Find and remove least recently used item
                lru_key = self.access_order.pop(0)
                del self.store[lru_key]
        
        self.store[key] = (value, expiry_time)
        self.access_order.append(key)

    def get(self, key):
        current_time = self.clock()
        
        if key not in self.store:
            return None
        
        value, expiry_time = self.store[key]
        
        # Check if entry is expired
        if current_time > expiry_time:
            # Remove expired entry
            del self.store[key]
            self.access_order.remove(key)
            return None
        
        # Entry is valid, update access order (move to end)
        self.access_order.remove(key)
        self.access_order.append(key)
        return value
