"""Levenshtein edit distance with two-row DP and early exits."""


def levenshtein(a: str, b: str) -> int:
    """Return the minimum edit distance between strings a and b.

    Uses two-row dynamic programming with early exits for optimal speed.
    Space complexity: O(min(len(a), len(b)))
    Time complexity: O(len(a) * len(b))
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