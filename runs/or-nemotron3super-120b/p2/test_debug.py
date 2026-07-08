from lru import LRUCache

class DebugLRUCache(LRUCache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.op = ""
    def _add_node(self, node):
        super()._add_node(node)
        self._debug("add", node.key)
    def _remove_node(self, node):
        self._debug("remove", node.key)
        super()._remove_node(node)
    def _move_to_head(self, node):
        self._debug("move_to_head", node.key)
        super()._move_to_head(node)
    def _pop_tail(self):
        node = self.tail.prev
        self._debug("pop_tail", node.key)
        return super()._pop_tail()
    def _debug(self, op, key):
        # print list
        cur = self.head.next
        vals = []
        while cur != self.tail:
            vals.append(str(cur.key))
            cur = cur.next
        print(f"{op}: {self.op} list: {'->'.join(vals)}", end='')
        if key is not None:
            print(f" node {key}", end='')
        print()
        self.op = ""

def test():
    cache = DebugLRUCache(2)
    cache.op = "put(1,1)"
    cache.put(1,1)
    cache.op = "put(2,2)"
    cache.put(2,2)
    cache.op = "put(1,10)"
    cache.put(1,10)
    print("get(1):", cache.get(1))
    cache.op = "get(2)"
    print("get(2):", cache.get(2))
    cache.op = "put(3,3)"
    cache.put(3,3)
    print("After put(3,3), get(2):", cache.get(2))
    print("After put(3,3), get(3):", cache.get(3))

if __name__ == "__main__":
    test()
