# P22 implement topological sort of a DAG with cycle detection
# toposort(n, edges) -> list or raises ValueError on cycle

def toposort(n, edges):
    # Build adjacency list and in-degree count
    adj = {i: [] for i in range(n)}
    in_degree = {i: 0 for i in range(n)}
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    # Initialize queue with nodes that have no incoming edges
    from collections import deque
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []
    
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        
        # Remove u from the graph
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    # If topological sort includes all nodes, no cycle exists
    if len(topo_order) == n:
        return topo_order
    else:
        raise ValueError("Cycle detected")