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
        # Move to end (most recent)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            # Update existing key and move to end
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        if len(self.cache) > self.capacity:
            # Pop the first item (least recent)
            self.cache.popitem(last=False)

