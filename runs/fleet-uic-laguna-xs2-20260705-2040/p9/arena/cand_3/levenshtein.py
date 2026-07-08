"""Levenshtein edit distance - optimized two-row DP with early exit."""


def levenshtein(a: str, b: str) -> int:
    """Return the edit distance between strings a and b.

    Uses two-row dynamic programming with early exit for optimal performance.
    Space complexity: O(min(m, n))
    Time complexity: O(m * n)
    """
    # Early exit: empty string cases
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
        b_char = b[j - 1]

        for i in range(1, m + 1):
            if a[i - 1] == b_char:
                curr[i] = prev[i - 1]
            else:
                curr[i] = 1 + min(prev[i],      # deletion
                                  curr[i - 1],   # insertion
                                  prev[i - 1])   # substitution

        prev, curr = curr, prev

    return prev[m]