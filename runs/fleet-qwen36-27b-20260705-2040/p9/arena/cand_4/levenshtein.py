"""
Levenshtein (edit) distance — candidate #4.

Distinct angle: two-row DP with a running-min early exit on the *current*
row.  The shorter string is always the column dimension.  After each row
we check whether  min(curr) + remaining_rows >= best_so_far, and if so
return immediately — the answer is already locked in.
"""

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between *a* and *b*."""

    # --- trivial cases ------------------------------------------------
    if a == b:
        return 0

    # Ensure `b` is the shorter string (columns = smaller dimension).
    if len(a) < len(b):
        a, b = b, a

    m, n = len(a), len(b)
    if n == 0:
        return m

    # --- two-row DP with early exit -----------------------------------
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    best = m  # upper bound: delete everything from a, insert all of b

    for i in range(1, m + 1):
        curr[0] = i
        remaining = m - i  # rows still to go after this one

        # Track the minimum value in the current row as we build it.
        min_curr = i  # starts with curr[0]

        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1]
            else:
                # min(prev[j-1], prev[j], curr[j-1]) + 1
                v = prev[j - 1]
                if prev[j] < v:
                    v = prev[j]
                if curr[j - 1] < v:
                    v = curr[j - 1]
                curr[j] = v + 1

            if curr[j] < min_curr:
                min_curr = curr[j]

        # Early exit: even the best cell in the current row, plus the
        # cheapest possible remaining operations (one deletion per row),
        # cannot beat the best complete answer seen so far.
        if min_curr + remaining >= best:
            return best

        # Update best with the last column of the current row.
        if curr[n] < best:
            best = curr[n]

        # Swap rows in-place (no allocation).
        prev, curr = curr, prev

    return prev[n]
