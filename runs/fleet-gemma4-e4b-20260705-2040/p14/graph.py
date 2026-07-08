# P14 SEED: BFS hop-count, ignores edge weights. Wrong on weighted graphs and
# returns hops not distance. Loop must implement weighted Dijkstra returning None/inf
# when unreachable.
import heapq

def shortest_path(n, edges, src, dst):
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        # Assuming undirected graph based on original implementation structure
        adj[u].append((v, w))
        adj[v].append((u, w))

    if src == dst:
        return 0

    dist = {i: float('inf') for i in range(n)}
    dist[src] = 0
    pq = [(0, src)]  # (distance, node)

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        for v, w in adj[u]:
            new_dist = dist[u] + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return dist[dst] if dist[dst] != float('inf') else -1
