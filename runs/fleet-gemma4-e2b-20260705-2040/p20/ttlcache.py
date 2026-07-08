from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        # store: {key: (value, expiry_time)}
        # order: OrderedDict to maintain LRU order (least recently used first)
        self.store = OrderedDict()

    def _is_expired(self, key):
        if key not in self.store:
            return True
        _, expiry_time = self.store[key]
        return self.clock.time() > expiry_time

    def get(self, key):
        if key not in self.store:
            return None
        
        # Check for TTL expiry on access (miss if expired)
        if self._is_expired(key):
            del self.store[key]
            return None
        
        # LRU update: move to end (most recently used)
        self.store.move_to_end(key)
        value, _ = self.store[key]
        return value

    def put(self, key, value, ttl):
        expiry_time = self.clock.time() + ttl
        
        if key in self.store:
            # Update existing item (update value and refresh TTL/LRU)
            self.store.move_to_end(key)
            self.store[key] = (value, expiry_time)
        else:
            # Check capacity and evict LRU if necessary
            if len(self.store) >= self.capacity:
                # Pop the first item (LRU)
                lru_key, _ = self.store.popitem(last=False)

            # Add new item
            self.store[key] = (value, expiry_time)

    def __len__(self):
        # Clean up expired items upon size check for robustness
        keys_to_delete = []
        for key, (_, expiry_time) in self.store.items():
            if self.clock.get_time() > expiry_time:
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            del self.store[key]
        
        return len(self.store)
