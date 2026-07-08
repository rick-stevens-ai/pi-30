"""
Fast Levenshtein distance implementation using a two‑row DP algorithm.
Works correctly for empty strings and identical inputs; early exits provided.
Standard library only.
"""

def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between strings ``a`` and ``b``."""
    # Trivial cases – early exit
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure we iterate over the shorter string in the inner loop for efficiency.
    if len(a) > len(b):
        a, b = b, a

    # v0 holds edit distances for empty prefix of ``b``
    v0 = list(range(len(a)+1))

    # Iterate over characters of ``b`` (the longer string)
    for i, ch_b in enumerate(b, start=1):
        # First cell: distance from empty prefix of a to this prefix of b
        v1 = [i] + [0]*len(a)

        # Compute distances for each character of ``a``
        for j, ch_a in enumerate(a, start=1):
            cost = 0 if ch_a == ch_b else 1
            # Minimum of deletion, insertion, substitution
            v1[j] = min(v1[j-1] + 1,          # deletion (left)
                        v0[j+1] + 1,           # insertion (above)
                        v0[j] + cost)            # substitution (diag)
        # Roll rows: current becomes previous for next iteration
        v0 = v1

    return v0[-1]