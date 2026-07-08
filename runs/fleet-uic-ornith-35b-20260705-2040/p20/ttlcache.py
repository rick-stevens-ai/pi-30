import collections


class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        # key -> (value, expiry), order reflects recency via put/get mutations
        self.store = collections.OrderedDict()

    def _maybe_expire(self):
        """Remove all expired entries from the underlying store."""
        now = self.clock()
        to_del = [k for k, (_, e) in self.store.items() if e <= now]
        for k in to_del:
            del self.store[k]

    def put(self, key, value, ttl):
        now = self.clock()
        expiry = now + ttl

        # Re-insert so it lands at MRU position
        if key in self.store:
            del self.store[key]
        self.store[key] = (value, expiry)

        # Drop expired entries globally.
        self._maybe_expire()

        # If still over the capacity bound, evict LRU-ish from front until within bounds.
        while len(self.store) > self.capacity:
            self.store.popitem(last=False)

    def get(self, key):
        if key not in self.store:
            return None
        value, expiry = self.store[key]
        now = self.clock()
        if expiry <= now:
            del self.store[key]
            return None
        # Touch for LRU tracking.
        self.store.move_to_end(key)
        return value
