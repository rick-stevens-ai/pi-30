from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        # Move to end to mark as most recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            # Update value and move to end
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                # Pop the first item (least recently used)
                self.cache.popitem(last=False)
            self.cache[key] = value
