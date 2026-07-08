"""Levenshtein edit distance with two-row DP and early exits."""


def levenshtein(a: str, b: str) -> int:
    """Return the minimum edit distance between strings a and b.
    
    Uses two-row dynamic programming with O(min(m,n)) space.
    Includes early exits for empty strings and identical inputs.
    """
    # Early exit: identical strings
    if a is b or a == b:
        return 0
    
    m, n = len(a), len(b)
    
    # Early exit: one empty string
    if m == 0:
        return n
    if n == 0:
        return m
    
    # Ensure 'a' is the shorter string to minimize space
    if m > n:
        a, b = b, a
        m, n = n, m
    
    # prev_row represents distances for empty prefix of a
    # curr_row is being built for each character of a
    prev_row = list(range(n + 1))
    curr_row = [0] * (n + 1)
    
    for i in range(1, m + 1):
        # First column: distance when b is empty (delete all chars from a)
        curr_row[0] = i
        
        # Get current character of a
        a_char = a[i - 1]
        
        for j in range(1, n + 1):
            # Cost is 0 if chars match, 1 otherwise
            cost = 0 if a_char == b[j - 1] else 1
            
            # Minimum of:
            # - deletion (prev_row[j] + 1)
            # - insertion (curr_row[j-1] + 1)
            # - substitution/match (prev_row[j-1] + cost)
            curr_row[j] = min(
                prev_row[j] + 1,        # deletion from a
                curr_row[j - 1] + 1,    # insertion to a
                prev_row[j - 1] + cost  # substitution or match
            )
        
        # Swap rows for next iteration
        prev_row, curr_row = curr_row, prev_row
    
    return prev_row[n]