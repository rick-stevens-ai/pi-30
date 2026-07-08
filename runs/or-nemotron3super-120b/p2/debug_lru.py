from lru import LRUCache

class DebugLRUCache(LRUCache):
    def _add_node(self, node):
        super()._add_node(node)
        self._debug("After _add_node", node.key)
    
    def _remove_node(self, node):
        self._debug("Before _remove_node", node.key)
        super()._remove_node(node)
        self._debug("After _remove_node", node.key)
    
    def _move_to_head(self, node):
        self._debug("Before _move_to_head", node.key)
        super()._move_to_head(node)
        self._debug("After _move_to_head", node.key)
    
    def _pop_tail(self):
        node = self.tail.prev
        self._debug("Before _pop_tail", node.key)
        res = super()._pop_tail()
        self._debug("After _pop_tail", node.key)
        return res
    
    def _debug(self, msg, key=None):
        # Print list from head to tail
        vals = []
        cur = self.head.next
        while cur != self.tail:
            vals.append(str(cur.key))
            cur = cur.next
        print(f"{msg}: {'->'.join(vals)}", end='')
        if key is not None:
            print(f" (node {key})", end='')
        print()

def test():
    cache = DebugLRUCache(2)
    print("put(1,1)")
    cache.put(1,1)
    print("put(2,2)")
    cache.put(2,2)
    print("get(1):", cache.get(1))
    print("put(1,10)")
    cache.put(1,10)
    print("put(3,3)")
    cache.put(3,3)
    print("get(1):", cache.get(1))
    print("get(2):", cache.get(2))
    print("get(3):", cache.get(3))

if __name__ == "__main__":
    test()
