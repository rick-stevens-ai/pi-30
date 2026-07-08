# P14 SEED: BFS hop-count, ignores edge weights. Wrong on weighted graphs and
# returns hops not distance. Loop must implement weighted Dijkstra returning -1
# when unreachable.
import heapq

def shortest_path(n, edges, src, dst):
    # Build adjacency list with weights
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w)); adj[v].append((u, w))
    
    if src == dst:
        return 0
    
    # Dijkstra's algorithm using priority queue
    dist = {i: float("inf") for i in range(n)}
    dist[src] = 0
    pq = [(0, src)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    
    return dist[dst] if dist[dst] != float("inf") else -1
