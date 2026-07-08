# Optimized using collections.Counter for O(n) counting.
from collections import Counter

def top_k(tokens, k):
    # Counter.most_common returns (elem, count) pairs sorted by count descending.
    return [w for w, _ in Counter(tokens).most_common(k)]
