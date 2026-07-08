class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation.

    - get(key): returns value or None if key not present, O(1)
    - put(key, value): inserts/update value; updates recency for existing keys
    - Both operations count as uses and affect eviction order.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        # Dictionary to store key -> Node mapping for O(1) access
        self.cache = {}
        # Dummy head and tail nodes to simplify boundary conditions
        self.head = DummyNode()
        self.tail = DummyNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node):
        """Add node right after head (most recently used)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        """Remove node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def get(self, key):
        """Get value by key; returns None if not found. O(1)."""
        node = self.cache.get(key)
        if node is None:
            return None
        # Move accessed node to head (most recently used)
        self._remove_node(node)
        self._add_to_head(node)
        return node.value

    def put(self, key, value):
        """
        Insert or update key->value.
        - If key exists: updates value and refreshes recency (move to head).
        - If full and new key: evict least recently used (tail.prev).
        """
        node = self.cache.get(key)
        if node is not None:
            # Update value and move to head
            node.value = value
            self._remove_node(node)
            self._add_to_head(node)
        else:
            # New key: create new node
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            if len(self.cache) > self.capacity:
                # Evict LRU (node before tail)
                lru_node = self.tail.prev
                self._remove_node(lru_node)
                del self.cache[lru_node.key]


class Node:
    """Doubly linked list node."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None  # type: ignore
        self.next = None  # type: ignore


class DummyNode:
    """Dummy node to simplify list boundaries."""
    def __init__(self):
        self.key = None
        self.value = None
        self.prev = None  # type: ignore
        self.next = None  # type: ignore
