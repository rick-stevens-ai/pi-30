# P22 topological sort of a DAG with cycle detection.
# toposort(n, edges) -> valid topological order (list of 0..n-1) or raises
# ValueError on a cycle (including self loops). edges: list of (u, v) meaning
# u must come before v.
def toposort(n, edges):
    # Build adjacency: u -> list of v (u before v), so v depends on u.
    adj = {i: [] for i in range(n)}
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    # Kahn's algorithm
    from collections import deque
    queue = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for w in adj[node]:
            indeg[w] -= 1
            if indeg[w] == 0:
                queue.append(w)

    if len(order) != n:
        raise ValueError("graph contains a cycle")
    return order
