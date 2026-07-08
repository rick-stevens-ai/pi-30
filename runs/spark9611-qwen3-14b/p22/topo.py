# P22 SEED: ignores edges entirely, returns 0..n-1. No cycle detection.
from collections import deque

def toposort(n, edges):
    graph = {i: [] for i in range(n)}
    in_degree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != n:
        raise ValueError("Cycle detected")

    return result
