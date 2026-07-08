# P20 SEED: a plain dict cache, no capacity enforcement, no TTL, ignores clock.
# Loop must add LRU eviction + TTL expiry using the injected clock.
from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        # OrderedDict: key -> (value, expiry_time)
        # Ordered from LRU (first) to MRU (last)
        self.store = OrderedDict()

    def _now(self):
        return self.clock()

    def _is_expired(self, expiry):
        return self._now() > expiry

    def _evict_expired(self, key=None):
        """Remove expired entries. If key is provided, only check that key."""
        if key is not None:
            if key in self.store and self._is_expired(self.store[key][1]):
                del self.store[key]
            return
        
        # Remove all expired entries
        expired_keys = [k for k, (_, exp) in self.store.items() if self._is_expired(exp)]
        for k in expired_keys:
            del self.store[k]

    def _evict_lru(self):
        """Evict the least recently used (first) entry."""
        if self.store:
            self.store.popitem(last=False)

    def _make_room(self):
        """Ensure there's room for a new entry, evicting expired first, then LRU."""
        # First, clean up expired entries
        self._evict_expired()
        # Then evict LRU until we have room
        while len(self.store) >= self.capacity:
            self._evict_lru()

    def _mark_mru(self, key):
        """Move key to MRU position (end of OrderedDict)."""
        value, expiry = self.store.pop(key)
        self.store[key] = (value, expiry)

    def put(self, key, value, ttl):
        now = self._now()
        expiry = now + ttl
        
        if key in self.store:
            # Update existing entry
            self.store[key] = (value, expiry)
            self._mark_mru(key)
        else:
            # New entry - make room if needed
            self._make_room()
            self.store[key] = (value, expiry)

    def get(self, key):
        if key not in self.store:
            return None
        
        value, expiry = self.store[key]
        
        if self._is_expired(expiry):
            del self.store[key]
            return None
        
        # Mark as MRU
        self._mark_mru(key)
        return value
