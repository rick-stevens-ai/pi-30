from collections import OrderedDict


class TTLCache:
    def __init__(self, capacity, ttl=None, clock=None):
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock
        self._data = OrderedDict()  # key -> (value, expiry)

    def _expired(self, expiry):
        if expiry is None:
            return False
        return self.clock() >= expiry

    def get(self, key):
        if key not in self._data:
            return None
        value, expiry = self._data[key]
        if self._expired(expiry):
            del self._data[key]
            return None
        self._data.move_to_end(key)
        return value

    def put(self, key, value, ttl=None):
        if ttl is None:
            ttl = self.ttl
        expiry = None if ttl is None else self.clock() + ttl
        if key in self._data:
            del self._data[key]
        self._data[key] = (value, expiry)
        self._data.move_to_end(key)
        # Evict LRU while over capacity.
        while len(self._data) > self.capacity:
            # Drop expired entries first if any.
            evicted = False
            for k, (v, e) in list(self._data.items()):
                if self._expired(e):
                    del self._data[k]
                    evicted = True
                    break
            if evicted:
                continue
            self._data.popitem(last=False)
