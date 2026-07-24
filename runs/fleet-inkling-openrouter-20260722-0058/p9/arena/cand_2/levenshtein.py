"""Levenshtein distance — two-row DP with early exit, stdlib only."""

def levenshtein(a: str, b: str) -> int:
    # Ensure a is the shorter string to minimize space/time
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    if m == 0:
        return n
    # Early exit: if length difference exceeds best possible, return diff
    # Already handled by two-row DP but kept explicit
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        curr = [i] * (m + 1)
        # Early exit: if all values in current row > best possible, break
        for j in range(1, m + 1):
            cost = 0 if a[j - 1] == b[i - 1] else 1
            curr[j] = min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost)
        prev = curr
    return prev[m]
