class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = {}  # key -> (value, expiry_time)
        self.order = []  # LRU order: front is LRU, back is MRU

    def _evict_expired(self):
        """Remove all expired entries from store and order."""
        now = self.clock()
        expired_keys = [k for k, (_, exp) in self.store.items() if now > exp]
        for k in expired_keys:
            del self.store[k]
            self.order.remove(k)

    def put(self, key, value, ttl):
        # First, evict expired entries so they don't count against capacity
        self._evict_expired()
        
        # If still at capacity, evict LRU
        if len(self.store) >= self.capacity:
            lru_key = self.order.pop(0)
            del self.store[lru_key]
        
        # Store the entry with its expiry time
        expiry = self.clock() + ttl
        self.store[key] = (value, expiry)
        self.order.append(key)

    def get(self, key):
        if key not in self.store:
            return None
        value, expiry = self.store[key]
        if self.clock() > expiry:
            # Expired - remove it
            del self.store[key]
            self.order.remove(key)
            return None
        # Move to MRU position
        self.order.remove(key)
        self.order.append(key)
        return value
