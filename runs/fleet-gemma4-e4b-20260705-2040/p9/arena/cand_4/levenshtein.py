def levenshtein(a: str, b: str) -> int:
    """
    Calculates the Levenshtein edit distance between two strings a and b using 
    a space-optimized (two-row DP) approach.

    Args:
        a: The first string.
        b: The second string.

    Returns:
        The minimum number of single-character edits (insertions, deletions or substitutions)
        required to change one word into the other.
    """
    len_a = len(a)
    len_b = len(b)

    # Handle trivial cases for empty strings
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Initialize the previous row (representing costs to transform an empty string into prefixes of b)
    # Size is len(b) + 1
    prev_row = list(range(len_b + 1))

    # Iterate through the characters of string 'a' (rows in conceptual matrix)
    for i in range(1, len_a + 1):
        current_row = [0] * (len_b + 1)
        # Initialize the first element of the current row (cost to transform prefix a[:i] into empty string b[:0])
        current_row[0] = i

        # Iterate through the characters of string 'b' (columns in conceptual matrix)
        for j in range(1, len_b + 1):
            # Cost for substitution: 0 if chars match, 1 otherwise
            cost = 0 if a[i - 1] == b[j - 1] else 1

            # Calculate the minimum cost using DP recurrence:
            # 1. Deletion (from prev_row): dp[i-1][j] + 1
            # 2. Insertion (from current_row, previous element): dp[i][j-1] + 1
            # 3. Substitution/Match (from prev_row, previous element): dp[i-1][j-1] + cost
            current_row[j] = min(
                prev_row[j] + 1,      # Deletion
                current_row[j - 1] + 1, # Insertion
                prev_row[j - 1] + cost  # Substitution/Match
            )

        # Update the previous row for the next iteration
        prev_row = list(current_row)
        
        # Optional: Early exit based on bounding box (if minimum value in current row exceeds known lower bound, 
        # though this is complex to implement correctly without potentially missing optimal paths if we only check a few points.
        # For simplicity and guaranteed correctness with two-row DP, we proceed unless performance profiling dictates otherwise.)

    return prev_row[len_b]

if __name__ == '__main__':
    # Example tests
    tests = [
        ("kitten", "sitting", 3),
        ("saturday", "sunday", 3),
        ("", "", 0),
        ("abc", "", 3),
        ("", "xyz", 3),
        ("test", "test", 0),
        ("a", "b", 1)
    ]

    print("--- Running Levenshtein Tests ---")
    all_passed = True
    for a, b, expected in tests:
        result = levenshtein(a, b)
        status = "PASSED" if result == expected else f"FAILED (Expected {expected}, Got {result})"
        print(f"Test '{a}' vs '{b}': {status}")
        if result != expected:
            all_passed = False
    
    print("----------------------------------")
    if all_passed:
        print("All tests passed successfully.")
    else:
        print("Some tests failed.")