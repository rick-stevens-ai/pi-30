def toposort(n, edges):
    indeg = {i: 0 for i in range(n)}
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    queue = [v for v in range(n) if indeg[v] == 0]
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for neighbor in adj[node]:
            indeg[neighbor] -= 1
            if indeg[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != n:
        raise ValueError("Cycle detected")
    return order
