# P15 SEED: O(n*V) using list.count for every unique token. Correct but very slow.
from collections import Counter
def top_k(text, k):
    tokens = [word.lower() for word in text]
    counts = Counter(tokens)
    # Sort by count descending, then word ascending
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return sorted_counts[:k]
