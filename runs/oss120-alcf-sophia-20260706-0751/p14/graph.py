# P14 SEED: BFS hop-count, ignores edge weights. Wrong on weighted graphs and
# returns hops not distance. Loop must implement weighted Dijkstra returning -1
# when unreachable.
import heapq
from typing import Dict, List, Tuple, Union


def shortest_path(*args) -> Union[int, float]:
    """Return the total weight of the minimum‑cost path.

    The function is flexible to support two calling conventions:

    1. ``shortest_path(n, edges, src, dst)`` where ``edges`` is a list of
       ``(u, v, w)`` tuples. This is the format used by the existing
       ``check.py`` script.
    2. ``shortest_path(graph, src, dst)`` where ``graph`` is a dictionary that
       maps a node to a list of ``(neighbor, weight)`` pairs. This matches the
       description in the problem statement.

    The implementation uses Dijkstra's algorithm with a ``heapq`` priority
    queue and works for non‑negative edge weights. If the destination is
    unreachable the function returns ``-1`` to stay compatible with the test
    harness (which expects ``-1`` for unreachable vertices)."""
    # Determine the calling convention.
    if isinstance(args[0], dict):
        # New signature: graph, src, dst
        graph: Dict[int, List[Tuple[int, int]]] = args[0]
        src: int = args[1]
        dst: int = args[2]
    else:
        # Legacy signature: n, edges, src, dst
        n: int = args[0]
        edges: List[Tuple[int, int, int]] = args[1]
        src: int = args[2]
        dst: int = args[3]
        # Build adjacency list from edge list.
        graph = {i: [] for i in range(n)}
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))

    if src == dst:
        return 0

    # Dijkstra's algorithm.
    dist = {node: float('inf') for node in graph}
    dist[src] = 0
    pq: List[Tuple[float, int]] = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == dst:
            # Early exit – shortest distance to dst found.
            break
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return dist[dst] if dist[dst] != float('inf') else -1
