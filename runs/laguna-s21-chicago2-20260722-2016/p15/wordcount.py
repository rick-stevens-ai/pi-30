# P15: O(n) counting via collections.Counter, then most_common (heapq.nlargest).
from collections import Counter

def top_k(tokens, k):
    return [w for w, _ in Counter(tokens).most_common(k)]
