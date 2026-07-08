class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # map key to Node
        # Dummy head and tail nodes
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node: Node) -> None:
        """Add node right after head (most recently used)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """Remove node from linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: Node) -> None:
        """Move node to head (most recently used)."""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        """Remove and return the least recently used node (before tail)."""
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key):
        """
        Return the value associated with the key if present, else None.
        Also mark the key as recently used.
        """
        node = self.cache.get(key)
        if not node:
            return None
        # Move the accessed node to the head (most recently used)
        self._move_to_head(node)
        return node.value

    def put(self, key, value) -> None:
        """
        Insert or update the value of the key.
        When the cache reaches capacity, invalidate the least recently used item.
        """
        node = self.cache.get(key)
        if node:
            # Update the value and move to head
            node.value = value
            self._move_to_head(node)
        else:
            # Create a new node
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)

            if len(self.cache) > self.capacity:
                # Remove the least recently used node
                tail = self._pop_tail()
                del self.cache[tail.key]