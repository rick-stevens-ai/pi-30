from collections import deque

def toposort(n, edges):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    
    for u, v in edges:
        if u == v:
            raise ValueError("self loop")
        adj[u].append(v)
        indeg[v] += 1
    
    # Kahn's algorithm (Kahn's algorithm)
    queue = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    
    if len(order) != n:
        raise ValueError("cycle detected")
    
    return order
