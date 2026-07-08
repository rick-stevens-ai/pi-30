from collections import Counter
import heapq

# P15 SEED: O(n) using Counter and heapq.nlargest. Much faster than O(n*V).
def top_k(tokens, k):
    counts = Counter(tokens)
    top_k_items = heapq.nlargest(k, counts.items(), key=lambda item: item[1])
    return [item[0] for item in top_k_items]
