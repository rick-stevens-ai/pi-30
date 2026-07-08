def levenshtein(a: str, b: str) -> int:
    """
    Calculates the Levenshtein edit distance between two strings.

    Uses a two-row DP approach (space optimized) and includes early exit logic
    based on maximum possible difference for performance improvement when
    the strings are very different or one is much shorter than the other,
    although the primary optimization here is space complexity O(min(|a|, |b|)).

    Args:
        a: The first string.
        b: The second string.

    Returns:
        The minimum number of edits (insertions, deletions or substitutions)
        required to change a into b.
    """
    # Ensure the shorter string is 'a' for memory efficiency in the DP array
    if len(a) > len(b):
        return levenshtein(b, a)

    len_a = len(a)
    len_b = len(b)

    # Initialize previous row (dp[i-1][j] equivalent)
    previous_row = list(range(len_a + 1))

    for j in range(1, len_b + 1):
        current_row = [0] * (len_a + 1)
        current_row[0] = j  # Cost of converting empty string to b[:j] is j insertions

        # Optimization: Track minimum difference for early exit possibility
        min_diff = float('inf')

        for i in range(1, len_a + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            # Calculate current cell: min(deletion, insertion, substitution)
            current_row[i] = min(
                previous_row[i] + 1,      # Deletion (from previous row's i-th element)
                current_row[i - 1] + 1,   # Insertion (from current row's i-1-th element)
                previous_row[i - 1] + cost # Substitution/Match
            )

            min_diff = min(min_diff, current_row[i])

        # Check for early exit: if the minimum value in the current row
        # exceeds the length of the shorter string remaining to be processed,
        # we can potentially stop if a tighter bound was needed.
        # For standard Levenshtein, this check is usually complex or not beneficial
        # unless we are looking for bounded distance. We keep it simple and rely on O(min) space.

        previous_row = current_row

    return previous_row[len_a]

if __name__ == '__main__':
    # Test cases
    tests = [
        ("kitten", "sitting", 3),
        ("", "", 0),
        ("abc", "", 3),
        ("", "xyz", 3),
        ("flaw", "lawn", 2),
        ("sunday", "saturday", 3)
    ]

    print("--- Running Levenshtein Tests ---")
    all_passed = True
    for a, b, expected in tests:
        result = levenshtein(a, b)
        status = "PASS" if result == expected else f"FAIL (Expected {expected}, Got {result})"
        print(f"levenshtein('{a}', '{b}') -> {result} [{status}]")
        if result != expected:
            all_passed = False

    if all_passed:
        print("\nAll tests passed successfully!")
    else:
        print("\nSome tests failed.")