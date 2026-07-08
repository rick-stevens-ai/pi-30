# Implement Dijkstra's algorithm for weighted undirected graphs.
# The function receives:
#   n: number of nodes (0 .. n-1)
#   edges: list of tuples (u, v, w) where w is a non‑negative weight
#   src: source node
#   dst: destination node
# It returns the total weight of the minimum‑cost path, or -1 if dst is unreachable.
# This matches the expectations of check.py (which uses -1 for unreachable).
import heapq

def shortest_path(n, edges, src, dst):
    # Build adjacency list with weights
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    if src == dst:
        return 0

    # Dijkstra's algorithm
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]  # (current_distance, node)
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == dst:
            # Early exit when we pop the destination with its shortest distance
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    # Unreachable
    return -1
