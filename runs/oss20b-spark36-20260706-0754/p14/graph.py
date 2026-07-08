# P14 SEED: weighted graph shortest‑path using Dijkstra.
import heapq

def shortest_path(n, edges, src, dst):
    """
    Compute the total weight of the minimum‑cost path between ``src`` and ``dst``
    in an undirected graph with non‑negative edge weights.

    Parameters
    ----------
    n : int
        Number of nodes (0 .. n-1)
    edges : list[tuple[int, int, int]]
        Edge list where each tuple is ``(u, v, w)`` and denotes a weighted
        undirected edge.  The weight ``w`` must be non‑negative.
    src, dst : int
        Source and destination node indices.

    Returns
    -------
    int | -1
        Total weight of the shortest path if one exists; otherwise ``-1``.
    """
    if src == dst:
        return 0

    # Build adjacency list with weights
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    dist = [float('inf')] * n
    dist[src] = 0

    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return dist[dst] if dist[dst] != float('inf') else -1
