def toposort(n, edges):
    # 1. Build graph (adjacency list) and calculate in-degrees
    adj = {i: [] for i in range(n)}
    in_degree = {i: 0 for i in range(n)}

    for u, v in edges:
        if v not in adj[u]: # Handle potential duplicate edges if necessary, though usually unnecessary for topo sort logic structure
            adj[u].append(v)
            in_degree[v] += 1

    # 2. Initialize queue with nodes having in-degree 0
    queue = [i for i in range(n) if in_degree[i] == 0]
    topo_order = []

    # 3. Process nodes (Kahn's algorithm)
    while queue:
        u = queue.pop(0)
        topo_order.append(u)

        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # 4. Check for cycles
    if len(topo_order) != n:
        raise ValueError("Graph has a cycle")
    
    return topo_order
