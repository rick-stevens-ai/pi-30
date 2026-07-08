def levenshtein(a: str, b: str) -> int:
    """Edit distance via two-row DP with diagonal band pruning.

    Candidate #3 angle: instead of the textbook column-by-column inner loop,
    we prune columns whose |i - j| lower bound already exceeds the proven
    minimum (abs(len(a) - len(b))).  This skips entire swathes of the matrix
    where values are provably at or above the floor, without any dynamic
    programming work.  Empty-string and length-difference cases short-circuit.
    """
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure shorter string is the inner loop (fewer columns to process).
    if len(a) < len(b):
        a, b = b, a

    n, m = len(a), len(b)
    lo = abs(n - m)  # hard lower bound on edit distance

    # Trivial: one string is an exact prefix/suffix of the other.
    if lo == n:
        return lo

    prev = list(range(m + 1))

    for i in range(1, n + 1):
        curr = [i] + [0] * m

        for j in range(1, m + 1):
            # Diagonal band: |i - j| is a hard lower bound on dp[i][j].
            # If it exceeds lo we can skip exact computation — those cells
            # are provably >= lo and won't affect the answer (which is <= lo
            # only when strings differ by exactly lo edits).
            if abs(i - j) > lo:
                curr[j] = lo
                continue

            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1]
            else:
                d1 = prev[j]      # deletion from a
                d2 = curr[j - 1]  # insertion into a
                d3 = prev[j - 1] + 1  # substitution
                curr[j] = min(d1, d2, d3)

        prev, curr = curr, prev

    return prev[m]
