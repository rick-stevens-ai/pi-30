# P14 SEED: BFS hop-count, ignores edge weights. Wrong on weighted graphs and
# returns hops not distance. Loop must implement weighted Dijkstra returning -1
# when unreachable.
import heapq

def shortest_path(n, edges, src, dst):
    # Build adjacency list with weights
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    # Dijkstra's algorithm
    if src == dst:
        return 0
    
    # Initialize distances to infinity
    dist = {i: float("inf") for i in range(n)}
    dist[src] = 0
    
    # Priority queue: (distance, node)
    heap = [(0, src)]
    
    while heap:
        current_dist, u = heapq.heappop(heap)
        
        # Skip if we already found a better path
        if current_dist > dist[u]:
            continue
        
        # Explore neighbors
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    
    # Return the shortest distance or -1 if unreachable
    return dist[dst] if dist[dst] != float("inf") else -1
