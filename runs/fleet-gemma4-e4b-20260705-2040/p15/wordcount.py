from collections import Counter
# P15 SEED: O(n*V) using list.count for every unique token. Correct but very slow.
def top_k(tokens, k):
    counts = Counter(tokens)
    return [word for word, count in counts.most_common(k)]
