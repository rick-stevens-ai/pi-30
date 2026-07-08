def levenshtein(a: str, b: str) -> int:
    """Edit distance via two-row DP with early termination."""
    la, lb = len(a), len(b)

    if la == 0: return lb
    if lb == 0: return la

    # Iterate over the shorter string to minimize outer-loop iterations.
    if la > lb:
        a, b = b, a
        la, lb = lb, la

    prev = list(range(la + 1))

    for i in range(1, lb + 1):
        curr = [i] * (la + 1)
        bi = b[i - 1]

        for j in range(1, la + 1):
            if a[j - 1] == bi:
                curr[j] = prev[j - 1]
            else:
                c, r, ins = prev[j - 1], curr[j], prev[j]
                m = min(c, r, ins)
                curr[j] = m + 1

        if curr[la] <= abs(la - lb):
            return curr[la]

    return curr[la]
