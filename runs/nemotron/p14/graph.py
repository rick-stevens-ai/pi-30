import heapq

def shortest_path(n, edges, src, dst):
    """Dijkstra's algorithm for shortest path in undirected weighted graph.
    
    Args:
        n: number of nodes (0 to n-1)
        edges: list of (u, v, w) tuples for undirected edges with weight w
        src: source node
        dst: destination node
    Returns:
        Shortest path distance from src to dst, or -1 if unreachable.
    """
    # Build adjacency list
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    # Dijkstra's algorithm with min-heap
    dist = {i: float('inf') for i in range(n)}
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
    
    return -1 if dist[dst] == float('inf') else dist[dst]