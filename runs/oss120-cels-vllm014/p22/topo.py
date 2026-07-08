# P22 SEED: implements a correct topological sort with cycle detection.
# toposort(n, edges) -> a list containing a valid topological order of the nodes 0..n-1.
# edges is an iterable of (u, v) pairs meaning u must come before v.
# Raises ValueError if the graph contains a cycle (including self‑loops).

def toposort(n, edges):
    """Return a topological ordering of a directed graph.

    Parameters
    ----------
    n : int
        Number of nodes, assumed to be labelled ``0`` … ``n-1``.
    edges : Iterable[Tuple[int, int]]
        Directed edges ``(u, v)`` indicating that ``u`` must appear before ``v``.

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
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        if u == v:
            # Self‑loop is a cycle.
            raise ValueError("self loop detected")
        # Guard against out‑of‑range vertices – let the algorithm raise IndexError naturally.
        adj[u].append(v)
        indeg[v] += 1

    # Kahn's algorithm: repeatedly remove nodes with indegree 0.
    from collections import deque
    zero = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while zero:
        node = zero.popleft()
        order.append(node)
        for nbr in adj[node]:
            indeg[nbr] -= 1
            if indeg[nbr] == 0:
                zero.append(nbr)

    if len(order) != n:
        # Not all nodes were processed -> cycle present.
        raise ValueError("graph contains a cycle")
    return order

