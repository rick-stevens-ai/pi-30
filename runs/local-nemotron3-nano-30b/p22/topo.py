# Proper topological sort with cycle detection
def toposort(n, edges):
    # Build adjacency list and indegree count
    adj = [[] for _ in range(n)]
    indeg = [0] * n

    # Process each edge; detect self-loop early
    for u, v in edges:
        if u == v:
            raise ValueError("Self loop detected")
        # Assuming nodes are within valid range 0..n-1
        adj[u].append(v)
        indeg[v] += 1

    # Initialize queue with nodes that have zero incoming edges
    from collections import deque
    q = deque([i for i in range(n) if indeg[i] == 0])
    
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nei in adj[node]:
            indeg[nei] -= 1
            if indeg[nei] == 0:
                q.append(nei)

    # If not all nodes were processed, a cycle exists
    if len(order) != n:
        raise ValueError("Cycle detected")
    
    return order