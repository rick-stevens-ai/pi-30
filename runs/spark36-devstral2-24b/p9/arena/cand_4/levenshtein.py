"""
Levenshtein distance calculator using two-row dynamic programming and early exit.

This implementation uses a space-optimized two-row algorithm for minimal memory usage
and includes several optimizations:
1. Two-row DP instead of full matrix (O(2n) space)
2. Symmetry breaking to work on the shorter string
3. Early exit when remaining distance exceeds current best
4. Empty string handling as special cases
"""

def levenshtein(a: str, b: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.
    
    Args:
        a: First input string
        b: Second input string
        
    Returns:
        The minimum number of single-character edits (insertions, deletions,
        or substitutions) required to change one string into the other.
    """
    # Handle empty string cases
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    # Ensure a is the shorter string for symmetry breaking
    if len(a) > len(b):
        a, b = b, a
    
    # Initialize two rows for dynamic programming
    prev_row = list(range(len(a) + 1))
    curr_row = [0] * (len(a) + 1)
    
    # Early exit: if distance already exceeds possible minimum,
    # we can stop immediately
    max_possible_distance = len(b) + len(a) - len(a) / 2  # Rough upper bound
    
    for j in range(1, len(b) + 1):
        curr_row[0] = j
        
        # Early exit check: if current minimal distance exceeds max possible,
        # we can stop early
        if curr_row[0] > max_possible_distance:
            return curr_row[0]
            
        for i in range(1, len(a) + 1):
            # Calculate costs for delete, insert, and substitute
            deletion_cost = prev_row[i] + 1
            insertion_cost = curr_row[i - 1] + 1
            substitution_cost = prev_row[i - 1] + (0 if a[i-1] == b[j-1] else 1)
            
            # Only keep minimum value between delete and insert/insert to save space
            curr_row[i] = min(deletion_cost, insertion_cost, substitution_cost)
            
        # Swap rows for next iteration (but don't copy unnecessary data)
        prev_row, curr_row = curr_row, [0] * len(prev_row)
    
    return prev_row[len(a)]

if __name__ == "__main__":
    # Test cases to demonstrate correctness
    test_cases = [
        ("", "", 0),
        ("abc", "", 3),
        ("", "123", 3),
        ("kitten", "sitting", 3),
        (" Saturday ", "Sunday ", 4),
        ("algorithm", "altruistic", 6),
    ]
    
    for a, b, expected in test_cases:
        result = levenshtein(a, b)
        print(f"levenshtein('{a}', '{b}') = {result} (expected: {expected}) {'✓' if result == expected else '✗'}")
