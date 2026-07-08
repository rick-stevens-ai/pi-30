# P15 SEED: O(n*V) using list.count for every unique token. Correct but very slow.
def top_k(tokens, k):
    from collections import Counter
    return [w for w, _ in Counter(tokens).most_common(k)]
