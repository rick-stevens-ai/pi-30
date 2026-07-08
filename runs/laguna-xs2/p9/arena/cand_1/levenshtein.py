"""Levenshtein edit distance with two-row DP and early exit."""


def levenshtein(a: str, b: str) -> int:
    """Return the edit distance between strings a and b.

    Uses optimized two-row dynamic programming with early exit for empty inputs.
    Space: O(min(m,n)), Time: O(m*n)
    """
    m, n = len(a), len(b)

    # Early exit for empty strings
    if m == 0:
        return n
    if n == 0:
        return m

    # Ensure we iterate over the shorter string for inner loop
    # This minimizes space to O(min(m,n))
    if m < n:
        a, b = b, a
        m, n = n, m

    # Two rows: previous and current
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr[j] = min(prev[j] + 1,          # deletion
                          curr[j - 1] + 1,      # insertion
                          prev[j - 1] + cost)   # substitution
        prev, curr = curr, prev

    return prev[n]