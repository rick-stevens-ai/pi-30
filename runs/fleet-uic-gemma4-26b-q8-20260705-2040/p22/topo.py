from collections import deque, defaultdict

def toposort(n, edges):
    adj = defaultdict(list)
    in_degree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    if len(order) != n:
        raise ValueError("Cycle detected")
    
    return order
