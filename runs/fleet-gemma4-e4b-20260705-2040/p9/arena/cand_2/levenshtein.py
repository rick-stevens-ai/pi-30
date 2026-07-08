def levenshtein(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein distance between two strings using 
    a space-optimized (two-row DP) approach.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        The minimum number of single-character edits (insertions, deletions or substitutions) 
        required to change one word into the other.
    """
    # Ensure s1 is the shorter string for space optimization
    if len(s1) > len(s2):
        return levenshtein(s2, s1)

    m = len(s1)
    n = len(s2)

    # Initialize the previous row (representing distances to empty prefix of s1)
    # Size is m + 1 (corresponding to prefixes of s1)
    prev_row = list(range(m + 1))

    # Iterate through characters of s2 (the longer string, defining rows in DP table)
    for i in range(1, n + 1):
        current_row = [i]  # Current row starts with distance 'i' (i insertions needed for s2[0..i-1] -> empty s1)

        # Iterate through characters of s1 (the shorter string, defining columns)
        for j in range(1, m + 1):
            # Cost of substitution/match
            cost = 0 if s1[j - 1] == s2[i - 1] else 1

            # DP recurrence:
            # Substitution cost (diagonal element from previous row)
            substitution_cost = prev_row[j - 1] + cost
            # Deletion cost (from previous row, same column index j)
            deletion_cost = prev_row[j] + 1
            # Insertion cost (from current row, previous column index j-1)
            insertion_cost = current_row[-1] + 1

            # Calculate the minimum distance
            min_dist = min(substitution_cost, deletion_cost, insertion_cost)
            current_row.append(min_dist)

        prev_row = current_row

    # The result is the last element of the final row
    return prev_row[m]

if __name__ == '__main__':
    # Test cases for correctness (including empty strings and simple cases)
    tests = [
        ("kitten", "sitting"),  # Expected: 3
        ("", ""),              # Expected: 0
        ("abc", ""),            # Expected: 3
        ("", "xyz"),            # Expected: 3
        ("a", "b"),             # Expected: 1
        ("same", "same"),       # Expected: 0
        ("algorithm", "altruistic"), # Expected: 6
    ]

    all_passed = True
    print("--- Running Levenshtein Tests ---")
    for s1, s2 in tests:
        result = levenshtein(s1, s2)
        expected = [3, 0, 3, 3, 1, 0, 6][tests.index((s1, s2))] if (s1, s2) in tests else None
        
        if expected is not None and result != expected:
            print(f"FAIL: levenshtein('{s1}', '{s2}') returned {result}, but expected {expected}")
            all_passed = False
        elif expected is not None:
             print(f"PASS: levenshtein('{s1}', '{s2}') == {result}")
        else:
             # Handle cases where I might miss the specific expected value if it wasn't in the predefined list above, though it should be.
             pass 

    if all_passed:
        print("\nAll tests passed successfully.")
    else:
        print("\nSome tests failed.")