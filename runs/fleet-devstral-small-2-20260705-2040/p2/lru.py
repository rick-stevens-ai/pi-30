class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.node_map = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.cache:
            return None
        node = self.node_map[key]
        self._remove_node(node)
        self._add_to_head(node)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            node = self.node_map[key]
            self._remove_node(node)
            self._add_to_head(node)
            self.cache[key] = value
            return
        if self.capacity <= 0:
            return
        if len(self.cache) >= self.capacity:
            lru_node = self.tail.prev
            self._remove_node(lru_node)
            del self.cache[lru_node.key]
            del self.node_map[lru_node.key]
        new_node = Node(key, value)
        self.cache[key] = value
        self.node_map[key] = new_node
        self._add_to_head(new_node)

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
