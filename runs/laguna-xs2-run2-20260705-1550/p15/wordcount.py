from collections import Counter
import heapq

def top_k(tokens, k):
    counts = Counter(tokens)
    return [w for w, _ in heapq.nlargest(k, counts.items(), key=lambda x: x[1])]

