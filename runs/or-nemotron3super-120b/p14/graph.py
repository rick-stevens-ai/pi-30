# P14: Dijkstra shortest path with heapq
import heapq

def shortest_path(n, edges, src, dst):
    # Build adjacency list
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    # Dijkstra
    INF = float('inf')
    dist = {i: INF for i in range(n)}
    dist[src] = 0
    pq = [(0, src)]  # (distance, node)
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == dst:
            return d  # early exit
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1 if dist[dst] == INF else dist[dst]
