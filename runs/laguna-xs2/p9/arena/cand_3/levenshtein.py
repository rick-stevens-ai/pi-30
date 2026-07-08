"""Levenshtein edit distance - optimized two-row DP with early exits."""


def levenshtein(a: str, b: str) -> int:
    """Compute the Levenshtein edit distance between two strings.

    Uses two-row dynamic programming for O(min(m,n)) space complexity.
    Includes early-exit optimizations for common cases.
    """
    # Early exit: identical strings
    if a == b:
        return 0

    # Ensure a is the shorter string for space efficiency
    m, n = len(a), len(b)
    if m > n:
        a, b = b, a
        m, n = n, m

    # Early exit: empty shorter string
    if m == 0:
        return n

    # Two-row DP with in-place updates
    # Use a single list, track previous values manually
    prev = list(range(m + 1))
    
    for j in range(1, n + 1):
        curr = [j]
        bj = b[j - 1]
        for i in range(1, m + 1):
            if a[i - 1] == bj:
                curr.append(prev[i - 1])
            else:
                curr.append(1 + min(prev[i], curr[i - 1], prev[i - 1]))
        prev = curr

    return prev[m]