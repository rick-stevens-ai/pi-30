# P22 SEED: ignores edges entirely, returns 0..n-1. No cycle detection.
from typing import List, Tuple

def toposort(n: int, edges: List[Tuple[int, int]]) -> List[int]:
    from collections import deque
    if n == 0:
        return []
    
    # Build adjacency list and in-degree dictionary
    adj = {i: [] for i in range(n)}
    in_degree = {i: 0 for i in range(n)}
    
    # Process edges
    for u, v in edges:
        if u == v:
            raise ValueError('Self-loop detected')
        adj[u].append(v)
        in_degree[v] += 1
    
    # Initialize queue with zero in-degree nodes
    queue = deque([node for node, degree in in_degree.items() if degree == 0])
    top_order = []
    
    while queue:
        u = queue.popleft()
        top_order.append(u)
        
        # Process all neighbors
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    # Check if graph has a cycle
    if len(top_order) != n:
        raise ValueError('Cycle detected')
    return top_order
