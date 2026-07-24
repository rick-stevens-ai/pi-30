# P14: Dijkstra shortest path using a min-heap (heapq).
# Returns the total weight of the minimum-cost path from src to dst,
# or -1 if dst is unreachable from src.
import heapq

def shortest_path(n, edges, src, dst):
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    dist = {i: float("inf") for i in range(n)}
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == dst:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return -1