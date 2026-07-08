def toposort(n, edges):
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = [i for i in range(n) if in_degree[i] == 0]
    # Use a list as a queue and pop from the front (or just iterate since order doesn't matter much)
    # Actually, to be safe with complexity, I should use collections.deque or just iterate through the current queue.
    
    topo_order = []
    # Since we don't need specifically BFS/DFS order as long as it's topo order, 
    # a simple list and pointer will do.
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        topo_order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(topo_order) < n:
        raise ValueError("Cycle detected")

    return topo_order
