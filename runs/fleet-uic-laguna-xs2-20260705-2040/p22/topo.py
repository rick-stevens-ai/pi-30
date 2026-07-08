def toposort(n, edges):
    """Return a valid topological order for a DAG, or raise ValueError if a cycle exists."""
    # Build adjacency list and in-degree count
    adj = {i: [] for i in range(n)}
    in_degree = {i: 0 for i in range(n)}
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    # Kahn's algorithm
    queue = [i for i in range(n) if in_degree[i] == 0]
    order = []
    
    while queue:
        node = queue.pop(0)
        order.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) != n:
        raise ValueError("cycle detected")
    
    return order