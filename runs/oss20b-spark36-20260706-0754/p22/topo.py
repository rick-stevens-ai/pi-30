def toposort(n, edges):
    """Return a topological ordering of the graph with n nodes and edge list.

    Args:
        n (int): number of nodes, numbered from 0..n-1.
        edges (list[tuple[int,int]]): directed edges (u,v) meaning u -> v.

    Returns:
        list[int]: a permutation of 0..n-1 which is a valid topological order.

    Raises:
        ValueError: if the graph contains a cycle (including self‑loops).
    """
    # Build adjacency list and indegree count
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        if u < 0 or v < 0 or u >= n or v >= n:
            raise ValueError("edge out of bounds")
        adj[u].append(v)
        indeg[v] += 1

    # Queue all nodes with indegree zero
    from collections import deque
    q = deque([i for i, d in enumerate(indeg) if d == 0])

    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    # If order doesn't contain all nodes, there's a cycle
    if len(order) != n:
        raise ValueError("cycle detected")
    return order
