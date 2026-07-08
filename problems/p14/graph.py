# P14 SEED: BFS hop-count, ignores edge weights. Wrong on weighted graphs and
# returns hops not distance. Loop must implement weighted Dijkstra returning -1
# when unreachable.
from collections import deque

def shortest_path(n, edges, src, dst):
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append(v); adj[v].append(u)
    if src == dst:
        return 0
    seen = {src}
    q = deque([(src, 0)])
    while q:
        node, hops = q.popleft()
        for nb in adj[node]:
            if nb == dst:
                return hops + 1
            if nb not in seen:
                seen.add(nb); q.append((nb, hops + 1))
    return -1
