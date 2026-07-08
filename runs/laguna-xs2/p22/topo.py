from collections import deque

def toposort(n, edges):
    # Build adjacency list and in-degree count
    adj = {i: [] for i in range(n)}
    in_degree = {i: 0 for i in range(n)}
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    # Start with nodes that have no incoming edges
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(result) != n:
        raise ValueError("Cycle detected")
    
    return result