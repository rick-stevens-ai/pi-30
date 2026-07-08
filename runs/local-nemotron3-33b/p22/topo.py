# P22 SEED: ignores edges entirely, returns 0..n-1. No cycle detection.
def toposort(n, edges):
    from collections import deque
    adj = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1
    q = deque([i for i in range(n) if indegree[i] == 0])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for neighbor in adj[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                q.append(neighbor)
    if len(order) != n:
        raise ValueError("cycle detected")
    return order