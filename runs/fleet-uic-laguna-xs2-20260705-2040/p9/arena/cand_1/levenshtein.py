"""Levenshtein edit distance - optimized two-row DP with early exit."""

def levenshtein(a: str, b: str) -> int:
    """Return the minimum edit distance between strings a and b."""
    # Early exits for trivial cases
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    # Early exit: if one is prefix of the other
    if a.startswith(b):
        return len(a) - len(b)
    if b.startswith(a):
        return len(b) - len(a)
    
    # Ensure we iterate over the shorter string in the outer loop
    # to minimize the working memory (two rows of length = shorter_len + 1)
    if len(a) < len(b):
        a, b = b, a
    
    m, n = len(a), len(b)
    
    # prev_row represents distances for empty prefix of a
    # curr_row is being built for each character of a
    prev_row = list(range(n + 1))
    curr_row = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr_row[0] = i  # cost of deleting all chars from a's prefix
        
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr_row[j] = prev_row[j - 1]
            else:
                curr_row[j] = 1 + min(
                    prev_row[j],      # deletion from a
                    curr_row[j - 1],  # insertion into a
                    prev_row[j - 1]   # substitution
                )
        
        prev_row, curr_row = curr_row, prev_row
    
    return prev_row[n]