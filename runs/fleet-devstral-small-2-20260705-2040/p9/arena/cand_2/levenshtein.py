def levenshtein(a: str, b: str) -> int:
    """Compute the Levenshtein edit distance between two strings.
    
    Uses a two-row dynamic programming approach for O(min(m,n)) space.
    Includes early exit if one string is empty.
    """
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    # Ensure a is the shorter string to minimize space
    if len(a) > len(b):
        a, b = b, a
    
    len_a, len_b = len(a), len(b)
    
    # Use two rows for DP: prev and curr
    prev = list(range(len_b + 1))
    curr = [0] * (len_b + 1)
    
    for i in range(1, len_a + 1):
        curr[0] = i
        
        for j in range(1, len_b + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr[j] = min(
                prev[j] + 1,      # deletion
                curr[j - 1] + 1,  # insertion
                prev[j - 1] + cost  # substitution
            )
        
        # Swap rows for next iteration
        prev, curr = curr, prev
    
    return prev[len_b]
