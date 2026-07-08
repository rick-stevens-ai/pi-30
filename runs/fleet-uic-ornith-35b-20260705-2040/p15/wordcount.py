from collections import Counter
def top_k(tokens, k):
    return [w for w, _ in Counter(tokens).most_common(k)]
