# P22 implementation: topological sort with cycle detection using Kahn's algorithm.
# toposort(n, edges) -> a list containing a valid topological order of the nodes 0..n-1.
# Raises ValueError if the graph contains a cycle (including self‑loops).

def toposort(n, edges):
    """Return a topological ordering of ``n`` nodes given directed ``edges``.

    Parameters
    ----------
    n : int
        Number of nodes, assumed to be labelled ``0`` through ``n-1``.
    edges : iterable of (int, int)
        Directed edges ``(u, v)`` meaning ``u`` must come before ``v``.

    Returns
    -------
    list[int]
        A permutation of ``range(n)`` that respects all dependencies.

    Raises
    ------
    ValueError
        If the graph contains a cycle (including a self‑loop).
    """

    # Build adjacency list and indegree count.
    adj = {i: [] for i in range(n)}
    indeg = [0] * n
    for u, v in edges:
        # Detect self‑loop early.
        if u == v:
            raise ValueError("self loop detected")
        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError("node index out of range")
        adj[u].append(v)
        indeg[v] += 1

    # Kahn's algorithm: repeatedly remove nodes with indegree 0.
    from collections import deque
    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(order) != n:
        # Not all nodes were processed -> cycle exists.
        raise ValueError("graph contains a cycle")
    return order

