"""Levenshtein edit distance — two-row DP with early exit."""

def levenshtein(a: str, b: str) -> int:
    """Return the minimum edit distance between *a* and *b*.

    Uses a space-optimised two-row DP table (O(min(n,m)) space) and
    an early-exit heuristic: if a full row equals the previous row
    the distance can no longer decrease, so the remaining cost is
    just the number of unmatched characters left in the longer string.
    """
    # Ensure `a` is the shorter string to minimise the inner loop.
    if len(a) > len(b):
        a, b = b, a

    la, lb = len(a), len(b)
    if la == 0:
        return lb

    # Two-row DP.  `prev` holds row i-1, `curr` is row i.
    prev = list(range(la + 1))

    # Pre-bind for speed.
    min_fn = min

    for j in range(1, lb + 1):
        curr = [0] * (la + 1)
        curr[0] = j
        bj = b[j - 1]

        for i in range(1, la + 1):
            if bj == a[i - 1]:
                curr[i] = prev[i - 1]
            else:
                curr[i] = min_fn(prev[i], prev[i - 1], curr[i - 1]) + 1

        # Early exit: if the entire row is identical to the previous row,
        # no further edits can reduce the distance.
        if curr == prev:
            return prev[la] + (lb - j)

        prev = curr

    return prev[la]
