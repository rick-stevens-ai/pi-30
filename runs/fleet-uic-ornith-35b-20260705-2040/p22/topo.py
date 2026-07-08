# P22 topological sort with cycle detection (Kahn's algorithm).
import collections


def toposort(n, edges):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        if u == v:
            raise ValueError(f"self-loop on node {u}")
        adj[u].append(v)
        indeg[v] += 1

    q = collections.deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(order) != n:
        raise ValueError("cycle detected")
    return order
