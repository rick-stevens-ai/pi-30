def levenshtein(a: str, b: str) -> int:
    """Compute the Levenshtein edit distance between two strings.
    
    Uses a two-row dynamic programming approach for memory efficiency.
    Implements early exit when one string is empty.
    
    Args:
        a: First string
        b: Second string
    
    Returns:
        The minimum edit distance (insertions, deletions, substitutions)
    """
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    len_a, len_b = len(a), len(b)
    
    # Use two rows to store the previous and current DP states
    prev_row = list(range(len_b + 1))
    curr_row = [0] * (len_b + 1)
    
    for i, char_a in enumerate(a):
        curr_row[0] = i + 1
        
        for j, char_b in enumerate(b):
            # Cost is 0 if characters match, 1 otherwise
            cost = 0 if char_a == char_b else 1
            
            # Minimum of three operations: insertion, deletion, substitution
            curr_row[j + 1] = min(
                prev_row[j + 1] + 1,      # Deletion
                curr_row[j] + 1,          # Insertion
                prev_row[j] + cost        # Substitution
            )
        
        # Swap rows for next iteration
        prev_row, curr_row = curr_row, prev_row
    
    return prev_row[len_b]


if __name__ == "__main__":
    # Test cases
    assert levenshtein("", "") == 0
    assert levenshtein("a", "") == 1
    assert levenshtein("", "a") == 1
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("saturday", "sunday") == 3
    assert levenshtein("hello", "hallo") == 1
    assert levenshtein("abc", "abc") == 0
    assert levenshtein("abc", "def") == 3
    assert levenshtein("abc", "x") == 3
    assert levenshtein("x", "abc") == 3
    
    print("All tests passed!")
