# P15 SEED: O(n*V) using list.count for every unique token. Correct but very slow.
def top_k(tokens, k):
    from collections import Counter
    c = Counter(tokens)
    return [w for w, _ in c.most_common(k)]
