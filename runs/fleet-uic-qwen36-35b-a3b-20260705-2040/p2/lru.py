class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        # Maps key -> node
        self._map = {}
        # Sentinel head and tail for the doubly linked list
        self._head = _Node(None, None)  # Most recent end (adjacent to first real item)
        self._tail = _Node(None, None)  # Least recent end (adjacent to last real item)
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    def get(self, key: int):
        node = self._map.get(key)
        if node is None:
            return None
        # Move to most-recent position (right after head sentinel)
        self._detach(node)
        self._attach_head(node)
        return node.value

    def put(self, key: int, value):
        node = self._map.get(key)
        if node is not None:
            # Key exists: update value and refresh recency
            node.value = value
            self._detach(node)
            self._attach_head(node)
        else:
            new_node = _Node(key, value)
            self._map[key] = new_node
            self._attach_head(new_node)
            self._size += 1
            if self._size > self.capacity:
                # Evict LRU (the node just before tail sentinel)
                victim = self._tail.prev
                self._detach(victim)
                del self._map[victim.key]
                self._size -= 1

    def _attach_head(self, node):
        """Insert *node* right after head sentinel."""
        nxt = self._head.next
        self._head.next = node
        node.prev = self._head
        node.next = nxt
        nxt.prev = node

    @staticmethod
    def _detach(node):
        """Remove *node* from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
