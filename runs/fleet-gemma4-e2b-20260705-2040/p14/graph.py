import heapq

def shortest_path(graph, _, src, dst):
    """
    Calculates the total weight of the min-cost path from src to dst using Dijkstra's algorithm.

    Args:
        graph (dict): Adjacency list representation {node: [(neighbor, weight), ...]}
        src (int): The source node.
        dst (int): The destination node.

    Returns:
        int or None: The total weight of the min-cost path, or None if unreachable.
    """
    if src == dst:
        return 0

    # Initialize distances to infinity for all nodes present in the graph keys
    distances = {node: float('inf') for node in graph}
    distances[src] = 0

    # Priority queue: (distance, node)
    pq = [(0, src)]

    while pq:
        dist, u = heapq.heappop(pq)

        if dist > distances[u]:
            continue

        if u in graph:
            for v, weight in graph[u]:
                new_dist = dist + weight
                
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))

    result = distances.get(dst, float('inf'))
    
    # Return None if unreachable, otherwise return the distance as an integer.
    return int(result) if result != float('inf') else None