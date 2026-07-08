"""Levenshtein edit distance - fast two-row DP implementation."""


def levenshtein(a: str, b: str) -> int:
    """Return the minimum edit distance between strings a and b.

    Uses two-row dynamic programming with early exits for optimal performance.
    Space: O(min(m,n)), Time: O(m*n)
    """
    # Early exits
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure 'a' is the shorter string to minimize space
    if len(a) > len(b):
        a, b = b, a

    m, n = len(a), len(b)

    # Two rows: previous and current
    prev = list(range(m + 1))
    curr = [0] * (m + 1)

    for j in range(1, n + 1):
        curr[0] = j
        bj = b[j - 1]

        for i in range(1, m + 1):
            if a[i - 1] == bj:
                curr[i] = prev[i - 1]
            else:
                d, i2, s = prev[i], curr[i - 1], prev[i - 1]
                min_val = d if d < i2 else i2
                curr[i] = 1 + (min_val if min_val < s else s)

        prev, curr = curr, prev

    return prev[m]