class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = {}  # key -> (value, expiry_time)
        self.lru = []    # list of keys in LRU order (front = LRU)

    def _cleanup_expired(self):
        """Remove all expired entries."""
        now = self.clock()
        expired = [k for k, (_, exp) in self.store.items() if now > exp]
        for k in expired:
            del self.store[k]
            self.lru.remove(k)

    def put(self, key, value, ttl):
        # Remove expired entries first (they don't count against capacity)
        self._cleanup_expired()
        
        # If key already exists, remove it from LRU list
        if key in self.store:
            self.lru.remove(key)
        
        # Evict LRU if at capacity
        if len(self.store) >= self.capacity:
            lru_key = self.lru.pop(0)
            del self.store[lru_key]
        
        # Store new entry with expiry time
        self.store[key] = (value, self.clock() + ttl)
        self.lru.append(key)

    def get(self, key):
        if key not in self.store:
            return None
        
        value, expiry = self.store[key]
        if self.clock() > expiry:
            # Expired - remove it
            del self.store[key]
            self.lru.remove(key)
            return None
        
        # Update LRU - move to end (MRU)
        self.lru.remove(key)
        self.lru.append(key)
        return value

