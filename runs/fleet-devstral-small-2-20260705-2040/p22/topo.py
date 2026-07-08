# P22 SEED: ignores edges entirely, returns 0..n-1. No cycle detection.
def toposort(n, edges):
    # Build adjacency list and in-degree count
    adj = {i: [] for i in range(n)}
    in_degree = {i: 0 for i in range(n)}
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    # Initialize queue with nodes that have no incoming edges
    queue = [i for i in range(n) if in_degree[i] == 0]
    result = []
    
    # Process nodes in topological order
    while queue:
        u = queue.pop(0)
        result.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    # If result doesn't contain all nodes, there's a cycle
    if len(result) != n:
        raise ValueError("Cycle detected in graph")
    
    return result
