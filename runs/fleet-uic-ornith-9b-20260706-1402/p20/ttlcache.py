from collections import OrderedDict


def _default_clock():
    import time
    def _clock():
        return float(time.time())
    return _clock


class TTLCache:
    """LRU cache with per-entry TTL expiry using an injectable clock."""

    def __init__(self, capacity, ttl=None, clock=None):
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock or _default_clock()
        self.store = OrderedDict()  # key -> [value, expiry_time]

    def put(self, key, value, ttl):
        now = self.clock()
        expiry = now + ttl if ttl is not None else now + float("inf")
        if key in self.store:
            # Update existing entry — do NOT move to MRU on put.
            self.store[key] = [value, expiry]
            return

        # Evict expired entries first (they don't count against capacity).
        while self.store:
            k = next(iter(self.store))
            _, expiry_time = self.store[k]
            if now >= expiry_time:
                del self.store[k]
            else:
                break

        # Now check capacity against only non-expired entries.
        while len(self.store) >= self.capacity and not self._is_expired(next(iter(self.store))):
            self.store.popitem(last=False)

        self.store[key] = [value, expiry]

    def get(self, key):
        if key not in self.store:
            return None
        value, expiry = self.store[key]
        now = self.clock()
        if now >= expiry:
            # Expired — return None but do NOT evict or re-order.
            return None
        # Access this entry: move to MRU (end of OrderedDict).
        self.store.move_to_end(key)
        return value

    def _is_expired(self, key):
        _, expiry = self.store[key]
        now = self.clock()
        return now >= expiry
