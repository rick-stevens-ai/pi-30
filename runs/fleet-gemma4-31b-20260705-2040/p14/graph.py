import heapq

def shortest_path(n, edges, src, dst):
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    
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
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
                
    return -1 if dist[dst] == float('inf') else dist[dst]
