def levenshtein(a: str, b: str) -> int:
    """Levenshtein edit distance with two-row DP and early exit."""
    if a == b:
        return 0
    # Ensure a is the shorter string to minimize space
    if len(a) > len(b):
        a, b = b, a
    n, m = len(a), len(b)
    if n == 0:
        return m

    # Two-row DP
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    for j in range(1, m + 1):
        curr[0] = j
        bj = b[j - 1]
        # Early exit: if all values exceed best possible remaining, break?
        # Instead compute row quickly and bail if row min >= best remaining
        row_min = j
        for i in range(1, n + 1):
            cost = 0 if a[i - 1] == bj else 1
            curr[i] = min(curr[i - 1] + 1, prev[i] + 1, prev[i - 1] + cost)
            if curr[i] < row_min:
                row_min = curr[i]
        prev, curr = curr, prev
    return prev[n]
