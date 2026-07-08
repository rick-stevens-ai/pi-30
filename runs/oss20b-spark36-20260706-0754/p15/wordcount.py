# P15 SEED: O(n*V) using list.count for every unique token. Correct but very slow.
def top_k(tokens, k):
    from collections import Counter
    import heapq
    c = Counter(tokens)
    return [w for w, _ in heapq.nlargest(k, c.items(), key=lambda x: x[1])]
