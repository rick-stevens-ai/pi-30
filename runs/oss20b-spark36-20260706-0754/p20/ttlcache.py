from collections import OrderedDict

class TTLCache:
    def __init__(self, capacity, clock):
        self.capacity = capacity
        self.clock = clock
        # OrderedDict preserves insertion order; we use it as a recency list.
        # key -> (value, expire_time)
        self.store: OrderedDict = OrderedDict()

    def put(self, key, value, ttl):
        """Insert or update an entry with the given TTL.

        If the cache is full, evict the least‑recently used non‑expired item.
        Expired items are simply removed; they do not count against capacity.
        """
        now = self.clock()
        expire_at = now + ttl

        if key in self.store:
            # Update existing entry and mark as most recently used
            self.store[key] = (value, expire_at)
            self.store.move_to_end(key)
            return

        # Evict items until there is space. Expired entries are discarded as we pop them.
        while len(self.store) >= self.capacity:
            lru_key, (_, lru_expire) = self.store.popitem(last=False)
            if now < lru_expire:
                # We evicted a valid LRU entry; capacity is now free
                break
            # else: expired entry was removed; continue checking next

        self.store[key] = (value, expire_at)

    def get(self, key):
        """Retrieve the value for *key* or ``None`` if missing/expired.

        Accessing a key updates its recency order.
        Expired entries are purged and treated as cache misses.
        """
        now = self.clock()
        item = self.store.get(key)
        if item is None:
            return None
        value, expire_at = item
        if now >= expire_at:
            # expired entry: remove it and report miss
            del self.store[key]
            return None
        # Mark as most recently used before returning
        self.store.move_to_end(key)
        return value