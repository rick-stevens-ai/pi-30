def levenshtein(a: str, b: str) -> int:
    """Compute the Levenshtein edit distance between two strings.
    
    Uses a two-row dynamic programming approach for memory efficiency
    and includes early exit when one string is empty.
    
    Args:
        a: First string
        b: Second string
    
    Returns:
        The minimum number of single-character edits (insertions, deletions, 
        or substitutions) required to change one string into the other.
    """
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    len_a, len_b = len(a), len(b)
    
    # Use two rows to store the DP table
    prev_row = list(range(len_b + 1))
    curr_row = [0] * (len_b + 1)
    
    for i in range(1, len_a + 1):
        curr_row[0] = i
        
        for j in range(1, len_b + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr_row[j] = min(
                prev_row[j] + 1,      # deletion
                curr_row[j - 1] + 1,  # insertion
                prev_row[j - 1] + cost  # substitution
            )
        
        # Swap rows for next iteration
        prev_row, curr_row = curr_row, prev_row
    
    return prev_row[len_b]
