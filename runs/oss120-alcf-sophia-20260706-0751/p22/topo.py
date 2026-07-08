# P22: Proper topological sort with cycle detection.
# toposort(n, edges) returns a list containing a valid topological ordering of the
# nodes 0..n-1 respecting the directed edges (u -> v). If the graph contains a
# cycle (including a self‑loop) a ValueError is raised.

def toposort(n, edges):
    """Return a topological ordering of a directed graph.

    Parameters
    ----------
    n : int
        Number of nodes, assumed to be labeled ``0`` through ``n-1``.
    edges : iterable of tuple(int, int)
        Directed edges ``(u, v)`` meaning *u* must come before *v*.

    Returns
    -------
    list[int]
        A permutation of ``range(n)`` that respects all edges.

    Raises
    ------
    ValueError
        If the graph contains a cycle (including a self‑loop).
    """
    # Build adjacency list and indegree count
    adj = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError("edge contains node out of range")
        adj[u].append(v)
        indegree[v] += 1

    # Kahn's algorithm: repeatedly remove nodes with indegree 0
    from collections import deque
    zero = deque([i for i, d in enumerate(indegree) if d == 0])
    order = []
    while zero:
        node = zero.popleft()
        order.append(node)
        for neigh in adj[node]:
            indegree[neigh] -= 1
            if indegree[neigh] == 0:
                zero.append(neigh)

    if len(order) != n:
        # Cycle detected
        raise ValueError("graph contains a cycle")
    return order

