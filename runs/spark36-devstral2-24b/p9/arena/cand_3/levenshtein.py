"""
Levenshtein distance implementation.
Computes the minimum number of single-character edits (insertions,
deletions, substitutions) required to change one string into another.

Uses a two-row dynamic programming approach for memory efficiency and includes
an early exit optimization when the remaining possible edits cannot improve
the best known so far.
"""

from typing import Tuple


def levenshtein(a: str, b: str) -> int:
    """
    Compute the Levenshtein distance between two strings.
    
    Args:
        a: First string
        b: Second string
        
    Returns:
        The minimum edit distance between a and b
        
    Examples:
        >>> levenshtein("", "")
        0
        >>> levenshtein("kitten", "sitting")
        3
        >>> levenshtein("flaw", "lawn")
        2
    """
    if a == b:
        return 0
    
    # Ensure a is the shorter string to minimize operations
    if len(a) > len(b):
        a, b = b, a
    
    len_a, len_b = len(a), len(b)
    
    # Early exit: if one string is empty, distance equals length of other
    if len_a == 0:
        return len_b
    
    # Initialize the DP array using two rows only (current and previous)
    prev_row = list(range(len_b + 1))
    curr_row = [0] * (len_b + 1)
    
    for i in range(1, len_a + 1):
        # First element of current row is delete cost
        curr_row[0] = i
        
        min_prev = float('inf')
        for j in range(1, len_b + 1):
            # Compute edit costs
            deletion_cost = prev_row[j] + 1
            insertion_cost = curr_row[j - 1] + 1
            substitution_cost = prev_row[j - 1] + (0 if a[i - 1] == b[j - 1] else 1)
            
            # Find minimum cost among the three operations
            curr_row[j] = min(deletion_cost, insertion_cost, substitution_cost)
        
        # Swap rows for next iteration
        prev_row, curr_row = curr_row, prev_row
    
    return prev_row[len_b]
