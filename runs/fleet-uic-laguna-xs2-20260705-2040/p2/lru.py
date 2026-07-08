"""LRU Cache implementation with O(1) operations using doubly linked list + hash map."""


class _Node:
    """Doubly linked list node for LRU cache."""

    __slots__ = ('key', 'value', 'prev', 'next')

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    Least Recently Used (LRU) cache with O(1) get and put operations.

    Both get and put count as uses. On existing key, put updates value and refreshes recency.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._cache = {}  # key -> _Node
        # Dummy head and tail for easier list manipulation
        self._head = _Node()  # most recently used (front)
        self._tail = _Node()  # least recently used (back)
        self._head.next = self._tail
        self._tail.prev = self._head

    def _remove(self, node: _Node) -> None:
        """Remove node from the linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: _Node) -> None:
        """Add node right after head (most recently used position)."""
        node.next = self._head.next
        node.prev = self._head
        self._head.next.prev = node
        self._head.next = node

    def get(self, key):
        """
        Get value by key, or None if not found.
        Moves accessed key to most-recently-used position.
        """
        if key not in self._cache:
            return None
        node = self._cache[key]
        # Move to front (most recently used)
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key, value):
        """
        Insert or update key-value pair.
        Updates existing key's value AND refreshes recency.
        Evicts LRU item if at capacity.
        """
        if key in self._cache:
            # Update existing node's value and move to front
            node = self._cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
        else:
            # Create new node
            node = _Node(key, value)
            self._cache[key] = node
            self._add_to_front(node)
            # Evict LRU if over capacity
            if len(self._cache) > self._capacity:
                lru_node = self._tail.prev
                self._remove(lru_node)
                del self._cache[lru_node.key]

    def __len__(self):
        return len(self._cache)

    def __contains__(self, key):
        return key in self._cache