from collections import deque


def toposort(n, edges):
    """Return a valid topological order of nodes 0..n-1.

    edges is a list of (u, v) pairs meaning u must appear before v.
    Raises ValueError if the graph contains a cycle (including self-loops).
    """
    adj = {i: [] for i in range(n)}
    indeg = {i: 0 for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    queue = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nb in adj[node]:
            indeg[nb] -= 1
            if indeg[nb] == 0:
                queue.append(nb)

    if len(order) != n:
        raise ValueError("graph contains a cycle")

    return order