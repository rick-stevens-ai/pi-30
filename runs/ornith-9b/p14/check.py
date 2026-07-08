# P14 oracle: Dijkstra shortest path vs a BFS-reference on unit graphs + a
# brute-force reference on small weighted graphs. Seed returns hop-count (ignores
# weights) so it fails on weighted graphs.
from graph import shortest_path
import random, itertools, heapq

def ref_dijkstra(n, edges, src, dst):
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w)); adj[v].append((u, w))
    dist = {i: float("inf") for i in range(n)}
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w; heapq.heappush(pq, (dist[v], v))
    return dist[dst] if dist[dst] != float("inf") else -1

def main():
    rng = random.Random(11)
    for t in range(400):
        n = rng.randint(2, 8)
        edges = []
        for u, v in itertools.combinations(range(n), 2):
            if rng.random() < 0.5:
                edges.append((u, v, rng.randint(1, 9)))
        src, dst = rng.randrange(n), rng.randrange(n)
        got = shortest_path(n, edges, src, dst)
        exp = ref_dijkstra(n, edges, src, dst)
        if got != exp:
            print(f"MISMATCH n={n} src={src} dst={dst} got={got} exp={exp} edges={edges}")
            raise SystemExit(1)
    print("OK P14")

if __name__ == "__main__":
    main()
