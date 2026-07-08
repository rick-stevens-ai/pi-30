# P14 SEED: BFS hop-count, ignores edge weights. Wrong on weighted graphs and
# returns hops not distance. Loop must implement weighted Dijkstra returning -1
# when unreachable.
from collections import deque

def shortest_path(n, edges, src, dst):
    import heapq
    graph = {i: [] for i in range(n)}
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    if src not in graph or dst not in graph:
        return float('inf')
    distances = {node: float('inf') for node in graph}
    distances[src] = 0
    heap = [(0, src)]
    while heap:
        current_dist, current_node = heapq.heappop(heap)
        if current_node == dst: return current_dist
        for neighbor, weight in graph[current_node]:
            if distances[neighbor] > current_dist + weight:
                distances[neighbor] = current_dist + weight
                heapq.heappush(heap, (distances[neighbor], neighbor))
    return float('inf')


