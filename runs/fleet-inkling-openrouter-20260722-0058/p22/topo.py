from collections import defaultdict, deque

def toposort(n, edges):
    graph = defaultdict(list)
    in_degree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    q = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                q.append(neighbor)
    if len(order) != n:
        raise ValueError("Cycle detected")
    return order
