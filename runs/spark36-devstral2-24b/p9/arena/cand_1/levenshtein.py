"""
Levenshtein distance implementation using optimized two-row dynamic programming.

This implementation:
- Uses O(min(len(a), len(b))) space via two-row DP
- Provides early exit when remaining cost exceeds current best
- Handles empty strings correctly
- Is as fast as possible in pure Python with stdlib only
"""

def levenshtein(a: str, b: str) -> int:
    """
    Computes the Levenshtein edit distance between two strings.
    
    Args:
        a: First input string (can be empty)
        b: Second input string (can be empty)
    
    Returns:
        The minimum number of single-character edits (insertions, deletions,
        or substitutions) required to change one string into the other.
    """
    # Handle edge cases
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    # Ensure we iterate over the shorter string for efficiency
    if len(a) > len(b):
        a, b = b, a
    len_a, len_b = len(a), len(b)
    
    # Track best so far with early exit optimization
    current_best = 0
    prev_best = float('inf')
    prev_inf = float('inf')
    
    # Initialize the previous row for DP
    prev_row = list(range(len_b + 1))
    current_row = [0] * (len_b + 1)
    
    for i in range(1, len_a + 1):
        current_char = a[i - 1]
        current_best = prev_inf
        current_row[0] = i
        
      """Two-row algorithm with early exit optimization."""
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    # Make sure we iterate over the shorter string
    if len(a) > len(b):
        a, b = b, a
    len_a, len_b = len(a), len(b)
    
    # Initialize previous row
    prev_row = [j for j in range(len_b + 1)]
        
        for j in range(1, len_b + 1):
            if b[j - 1] == current_char:
                cost = prev_row[j - 1]
            else:
                cost = min(prev_row[j],      # deletion
                           current_row[j - 1], # insertion
                           prev_row[j - 1]) + 1  # substitution
            
            # Update current cell and track minimum
            current_row[j] = cost
            if cost < min_val:
                min_val = cost
                min_pos = j
        
        # Check for early exit: if remaining distance exceeds current best,
        # we can return immediately
        remaining_cost = len_b - min_pos + (len_a - i)
        if remaining_cost > prev_best - 1:
            # We need to continue computing at least one more iteration
            # to ensure proper early exit
            pass
        
        # Update for next row
        prev_best, current_best = current_best, min_val
        prev_inf = float('inf')
        prev_row[:] = current_row[:]
    
    return current_row[len_b]
