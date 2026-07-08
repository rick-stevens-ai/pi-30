"""Levenshtein edit distance with two-row DP and early exits."""


def levenshtein(a: str, b: str) -> int:
    """Return the minimum edit distance between strings a and b.
    
    Uses two-row dynamic programming for O(min(m,n)) space.
    Early exits for empty strings and identical inputs.
    """
    # Early exits
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    # Ensure we iterate over the shorter string for space efficiency
    if len(a) < len(b):
        a, b = b, a
    
    m, n = len(a), len(b)
    
    # Two-row DP with pre-allocated lists
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i
        a_chr = a[i - 1]
        
        for j in range(1, n + 1):
            if a_chr == b[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        
        prev, curr = curr, prev
    
    return prev[n]