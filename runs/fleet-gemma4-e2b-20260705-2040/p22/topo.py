def toposort(n, edges):
    """
    Computes a topological order of the graph defined by n nodes and a list of directed edges.
    Raises ValueError if a cycle is detected.

    Args:
        n (int): The number of nodes (0 to n-1).
        edges (list[tuple[int, int]]): A list of directed edges (u, v) meaning u -> v.

    Returns:
        list[int]: A valid topological ordering of the nodes.

    Raises:
        ValueError: If the graph contains a cycle.
    """
    adj = [[] for _ in range(n)]
    in_degree = [0] * n

    # Build adjacency list and in-degree counts
    for u, v in edges:
        if 0 <= u < n and 0 <= v < n:
            adj[u].append(v)
            in_degree[v] += 1

    # Initialize queue with nodes having an in-degree of 0
    queue = [i for i in range(n) if in_degree[i] == 0]
    topological_order = []
    count = 0

    while queue:
        u = queue.pop(0)
        topological_order.append(u)
        count += 1

        # Process neighbors
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # Check for cycle
    if count != n:
        raise ValueError("Graph contains a cycle, cannot produce a topological sort.")

    return topological_order