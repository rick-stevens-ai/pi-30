"""Levenshtein edit distance with two-row DP and early exits."""
from array import array


def levenshtein(a, b) -> int:
    """Return the Levenshtein edit distance between a and b.

    Uses two-row dynamic programming with early exit optimizations.
    Correctly handles empty strings and all input types supporting len() and indexing.
    """
    # Early exit: identical objects
    if a is b:
        return 0

    m, n = len(a), len(b)

    # Early exit: one empty
    if m == 0:
        return n
    if n == 0:
        return m

    # Ensure we iterate over the shorter string for cache efficiency
    if m < n:
        a, b = b, a
        m, n = n, m

    # Two-row DP using array for better cache performance
    previous = array('I', range(n + 1))
    current = array('I', [0] * (n + 1))

    for j in range(1, m + 1):
        current[0] = j
        prev_diag = previous[0]

        for i in range(1, n + 1):
            prev_diag_save = previous[i]
            if a[j - 1] == b[i - 1]:
                current[i] = prev_diag
            else:
                current[i] = 1 + min(previous[i],      # deletion
                                     current[i - 1],    # insertion
