def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between strings a and b.
    Uses two‑row DP with early exit for trivial cases.
    """
    # Fast paths
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure that b is the longer string to minimise space
    if len(a) > len(b):
        a, b = b, a

    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i] + [0] * len(b)
        # Optional optimisation: if the smallest value in current row
        # already exceeds the best possible distance we could achieve,
        # we could break early, but for exact distance we keep it simple.
        for j, cb in enumerate(b, 1):
            insert = previous[j] + 1          # insert ca
            delete = current[j - 1] + 1       # delete cb
            replace = previous[j - 1] + (ca != cb)  # substitute if needed
            current[j] = min(insert, delete, replace)
        previous = current
    return previous[-1]