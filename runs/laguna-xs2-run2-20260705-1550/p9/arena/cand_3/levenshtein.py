"""Levenshtein edit distance with two-row DP and early exit optimizations."""

def levenshtein(a: str, b: str) -> int:
    """Return the minimum edit distance between strings a and b.
    
    Uses two-row dynamic programming with early exit for optimal performance.
    Correct for all inputs including empty strings.
    """
    # Early exits for edge cases
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    m, n = len(a), len(b)
    
    # Ensure we iterate over the shorter string in the inner loop
    # This minimizes memory and comparisons
    if m < n:
        a, b = b, a
        m, n = n, m
    
    # Two rows: previous and current
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i
        for