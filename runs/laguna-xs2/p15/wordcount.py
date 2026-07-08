# P15 SEED: O(n*V) using list.count for every unique token. Correct but very slow.
import collections, heapq

def top_k(tokens, k):
    counts = collections.Counter(tokens)
    return [w for w, _ in heapq.nlargest(k, counts.items(), key=lambda x: x[1])]

