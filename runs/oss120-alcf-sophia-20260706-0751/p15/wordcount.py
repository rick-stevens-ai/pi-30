# Optimized top_k using collections.Counter for O(n) performance.
from collections import Counter

def top_k(tokens, k):
    # Counter.most_common returns (element, count) sorted by count descending.
    # This matches the reference implementation's ordering.
    return [word for word, _ in Counter(tokens).most_common(k)]
