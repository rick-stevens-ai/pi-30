def toposort(n, edges):
    # Build adjacency list and in-degree count
    adj = {i: [] for i in range(n)}
    in_degree = {i: 0 for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    # Kahn's algorithm: start with nodes having in-degree 0
    queue = [i for i in range(n) if in_degree[i] == 0]
    result = []
    
    while queue:
        node = queue.pop(0)
        result.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If not all nodes processed, there's a cycle
    if len(result) != n:
        raise ValueError("Graph contains a cycle")
    
    return result

