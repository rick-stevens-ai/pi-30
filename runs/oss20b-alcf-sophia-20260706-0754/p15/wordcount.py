# P15 SEED: O(n*V) using list.count for every unique token. Correct but very slow.
def top_k(tokens, k):
    import collections, heapq
    counter = collections.Counter(tokens)
    return [w for w,_ in heapq.nlargest(k, counter.items(), key=lambda x: x[1])]
