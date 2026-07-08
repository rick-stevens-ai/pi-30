# P2 external verifier — the agent must ALSO ship its own bundled tests, but this
# independent verifier confirms the LRU cache actually behaves correctly.
from lru import LRUCache

def main():
    c = LRUCache(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1            # 1 used, 2 is now LRU
    c.put(3, 3)                     # evicts 2
    assert c.get(2) is None
    c.put(4, 4)                     # evicts 1 (3 was just... 1 was used at get)
    assert c.get(1) is None
    assert c.get(3) == 3
    assert c.get(4) == 4
    # update existing key counts as use and updates value
    c2 = LRUCache(2)
    c2.put("a", 1); c2.put("b", 2); c2.put("a", 10)  # a refreshed
    c2.put("c", 3)                  # evicts b
    assert c2.get("b") is None
    assert c2.get("a") == 10
    assert c2.get("c") == 3
    # capacity 1 edge
    c3 = LRUCache(1)
    c3.put(1, 1); c3.put(2, 2)
    assert c3.get(1) is None and c3.get(2) == 2
    print("OK P2")

if __name__ == "__main__":
    main()
