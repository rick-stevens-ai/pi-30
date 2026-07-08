# P15 SEED: O(n*V) using list.count for every unique token. Correct but very slow.
def top_k(tokens, k):
    uniq = []
    for t in tokens:
        if t not in uniq:
            uniq.append(t)
    counts = [(w, tokens.count(w)) for w in uniq]   # O(n) scan per unique word
    counts.sort(key=lambda x: x[1], reverse=True)
    return [w for w, _ in counts[:k]]
