# P20 iterate-until-green: LRU cache WITH per-entry TTL expiry. 
# get(k) returns None if expired; put(k,v,ttl). Uses an injectable clock so tests
# are deterministic. Seed has no TTL at all. Verdict = pytest exit code.
from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        self.store = OrderedDict()  # key -> (value, expires_at)

    def put(self, key, value, ttl):
        expires = self.clock() + ttl
        if key in self.store:
            # update value and expiry time, keep order unchanged for now
            _, _ = self.store[key]  # dummy to keep tuple unpacking; will replace below
            self.store[key] = (value, expires)
        else:
            self.store[key] = (value, expires)

        # If over capacity, evict LRU (least recently used) entry(s)
        while len(self.store) > self.capacity:
            # popitem(last=False) removes the first inserted/last accessed item
            evicted_key, _ = self.store.popitem(last=False)
            # No need to handle expiry; eviction respects current size

    def get(self, key):
        if key not in self.store:
            return None

        value, expires_at = self.store[key]
        current_time = self.clock()

        if current_time >= expires_at:
            # expired – remove and treat as miss
            del self.store[key]
            return None
        else:
            # move to end to mark as most recently used
            self.store.move_to_end(key)
            return value