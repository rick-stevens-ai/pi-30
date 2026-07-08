"""Levenshtein edit distance — two-row DP with early-exit pruning."""

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein (edit) distance between *a* and *b*.

    Optimisations
    -------------
    * **Two-row DP** — only two rows of length ``min(m, n) + 1`` are kept.
    * **Early exit** — after each row the minimum value is tracked; if that
      minimum already exceeds the best full-row answer found so far the
      algorithm can stop (the remaining rows can only increase the distance).
    * **Short string on the inside** — *b* is always the shorter string so
      the inner array is as small as possible.
    """
    # --- ensure b is the shorter string (smaller inner array) ---
    if len(a) < len(b):
        a, b = b, a

    m, n = len(a), len(b)

    if n == 0:
        return m

    # --- two-row DP (previous / current) ---
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    best = m  # upper bound: full deletions of the remaining chars of a

    for i in range(1, m + 1):
        curr[0] = i
        row_min = i  # tracks the smallest value in this row

        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cost = 0
            else:
                cost = 1

            # inline min of three candidates
            ins = curr[j - 1] + 1
            dele = prev[j] + 1
            sub = prev[j - 1] + cost

            if ins <= dele:
                val = ins if ins <= sub else sub
            else:
                val = dele if dele <= sub else sub

            curr[j] = val
            if val < row_min:
                row_min = val

        # --- early exit: if the smallest value in this row is already
        #     >= best, no future row can improve on best (row_min is
        #     non-decreasing as we move down the matrix) ---
        if row_min >= best:
            break

        if row_min < best:
            best = row_min

        # swap rows in-place (O(1))
        prev, curr = curr, prev

    # after the loop prev holds the last computed row
    return min(prev) if row_min < best else best
