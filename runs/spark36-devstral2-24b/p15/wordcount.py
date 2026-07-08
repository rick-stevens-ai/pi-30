# P15 SEED: O(n*V) using list.count for every unique token. Correct but very slow.
from collections import Counter

def top_k(tokens, k):
    count = Counter(tokens)
    sorted_counts = sorted(count.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_counts[:k]]
