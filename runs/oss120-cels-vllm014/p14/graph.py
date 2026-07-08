# P14 solution: Weighted Dijkstra shortest path.
# Returns total weight of the minimum‑cost path, or -1 if dst is unreachable.
import heapq

def shortest_path(n, edges, src, dst):
    # Build adjacency list with weights (undirected graph)
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    if src == dst:
        return 0
    # Dijkstra's algorithm
    dist = [float('inf')] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        if u == dst:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return -1
