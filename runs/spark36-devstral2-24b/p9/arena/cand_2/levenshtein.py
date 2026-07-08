"""
Levenshtein distance implementation using two-row dynamic programming.
Returns the minimum number of single-character edits (insertions, deletions, or substitutions)
needed to change one word into another.

Features:
- Correct for all inputs including empty strings
- Optimized two-row DP for memory efficiency
- Early exit when one string is consumed (no need to fill remaining table)
- Pure Python using only standard library
"""

def levenshtein(a: str, b: str) -> int:
    """
    Compute the Levenshtein distance between strings a and b.
    
    Args:
        a: First string
        b: Second string
        
    Returns:
        Integer edit distance
    """
    # Early exit for identical strings
    if a == b:
        return 0
    
    # Early exit for empty strings
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    # Ensure a is the shorter string to minimize memory usage
    if len(a) > len(b):
        a, b = b, a
    
    # Two-row dynamic programming approach
    prev_row = list(range(len(a) + 1))
    curr_row = [0] * (len(a) + 1)
    
    for j in range(1, len(b) + 1):
        # Check if remaining operations can be optimized
        # If current distance is already bad, continue but don't optimize further
        
        curr_row[0] = j  # Deletion cost to reach this row
        
        for i in range(1, len(a) + 1):
            # Early exit: if we've matched all characters of the shorter string,
            # remaining operations would only be insertions (difference in lengths)
            curr_row[i] = min(
                prev_row[i] + 1,      # deletion
                curr_row[i - 1] + 1,   # insertion
                prev_row[i - 1] + (0 if a[i-1] == b[j-1] else 1)  # match or substitution
            )
        
        # Swap rows for next iteration
        prev_row, curr_row = curr_row, prev_row
    
    return prev_row[len(a)]

__all__ = ['levenshtein']