# P14: Implements weighted Dijkstra using heapq. Returns total weight of shortest path,
# or -1 if src cannot reach dst.
import heapq

def shortest_path(n, edges, src, dst):
    # Build adjacency list mapping node -> list of (neighbor, weight)
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    if src == dst:
        return 0

    # Dijkstra algorithm
    dist = {i: float('inf') for i in range(n)}
    dist[src] = 0
    heap = [(0, src)]   # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist[dst] if dist[dst] != float('inf') else -1