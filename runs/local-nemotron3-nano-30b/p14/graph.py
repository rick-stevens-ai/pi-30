# P14 SEED: BFS hop-count, ignores edge weights. Wrong on weighted graphs and
# returns hops not distance. Loop must implement weighted Dijkstra returning -1
# when unreachable.
from collections import deque

import heapq

def shortest_path(n, edges, src, dst):
    # Build adjacency list of (neighbor, weight) tuples.
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    INF = float('inf')
    dist = [INF] * n
    visited = [False] * n
    dist[src] = 0.0

    heap = [(0.0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        if u == dst:
            return d   # numeric distance (int or float)
        for v, w in adj[u]:
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))

    # Unreachable.
    return -1