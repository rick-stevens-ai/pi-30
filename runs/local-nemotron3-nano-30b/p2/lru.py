from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = max(0, capacity)
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return None
        # Move to end to mark as most recently used
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.cache:
            # Update value and move to most recent
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                # Remove least recently used item
                self.cache.popitem(last=False)
            self.cache[key] = value