class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = {}  # key -> (value, expires_at)
        self.lru = []    # list of keys in LRU order (front = LRU, back = MRU)

    def _is_expired(self, key):
        if key not in self.store:
            return True
        _, expires_at = self.store[key]
        return self.clock() >= expires_at

    def _evict_expired(self):
        """Remove expired entries, returning True if any were removed."""
        expired = [k for k in self.store if self._is_expired(k)]
        for k in expired:
            del self.store[k]
            if k in self.lru:
                self.lru.remove(k)
        return len(expired) > 0

    def _evict_lru(self):
        """Evict the LRU entry that is not expired."""
        for k in self.lru:
            if not self._is_expired(k):
                del self.store[k]
                self.lru.remove(k)
                return

    def put(self, key, value, ttl):
        # Remove from LRU if already present
        if key in self.lru:
            self.lru.remove(key)
        
        # Evict expired entries first
        self._evict_expired()
        
        # If at capacity, evict LRU
        if len(self.store) >= self.capacity:
            self._evict_lru()
        
        # Store entry with expiration time
        expires_at = self.clock() + ttl
        self.store[key] = (value, expires_at)
        self.lru.append(key)  # Add to MRU position

    def get(self, key):
        if key not in self.store:
            return None
        if self._is_expired(key):
            del self.store[key]
            if key in self.lru:
                self.lru.remove(key)
            return None
        # Move to MRU position
        self.lru.remove(key)
        self.lru.append(key)
        return self.store[key][0]