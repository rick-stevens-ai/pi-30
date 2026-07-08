from collections import Counter

def top_k(tokens, k):
    counts = Counter(tokens)
    return [w for w, _ in counts.most_common(k)]
