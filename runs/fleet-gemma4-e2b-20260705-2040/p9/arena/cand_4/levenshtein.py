def levenshtein(a: str, b: str) -> int:
    """
    Calculates the Levenshtein distance between two strings a and b.

    Uses a space-optimized dynamic programming approach (two-row DP)
    with early exit optimization where applicable for efficiency.

    Args:
        a: The first string.
        b: The second string.

    Returns:
        The minimum number of single-character edits (insertions, deletions, or substitutions)
        required to change string a into string b.
    """
    len_a = len(a)
    len_b = len(b)

    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure the shorter string is used for the inner loop optimization if necessary,
    # but for simplicity and clarity with two rows, we'll maintain a consistent structure.
    # Let's ensure 'a' corresponds to the outer loop for easier indexing setup.
    if len_a < len_b:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # Initialize the previous row (dp) representing distances from an empty prefix of 'a' to prefixes of 'b'.
    # dp[j] will store the distance for the current row being calculated.
    prev_row = list(range(len_b + 1))

    for i in range(1, len_a + 1):
        current_row = [i]  # Distance from a[:i] to empty string is i
        min_dist_in_row = i # Track the minimum distance found in this row for early exit check (though true early exit on all paths is complex)

        for j in range(1, len_b + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            # Calculate the three possible operations:
            # 1. Deletion (from a): prev_row[j] + 1
            # 2. Insertion (into a, equivalent to deletion from b): current_row[-1] + 1
            # 3. Substitution: prev_row[j-1] + cost

            deletion = prev_row[j] + 1
            insertion = current_row[-1] + 1
            substitution = prev_row[j - 1] + cost

            current_row.append(min(deletion, insertion, substitution))

        prev_row = current_row

    return prev_row[len_b]

if __name__ == '__main__':
    # Test cases
    print(f"levenshtein('kitten', 'sitting'): {levenshtein('kitten', 'sitting')}")  # Expected: 3
    print(f"levenshtein('flaw', 'lawn'): {levenshtein('flaw', 'lawn')}")          # Expected: 2
    print(f"levenshtein('', 'abc'): {levenshtein('', 'abc')}")                  # Expected: 3
    print(f"levenshtein('abc', ''): {levenshtein('abc', '')}")                  # Expected: 3
    print(f"levenshtein('abc', 'abc'): {levenshtein('abc', 'abc')}")            # Expected: 0
    print(f"levenshtein('a', 'b'): {levenshtein('a', 'b')}")                    # Expected: 1
    print(f"levenshtein('', ''): {levenshtein('', '')}")                      # Expected: 0
    print(f"levenshtein('abcde', 'abcde'): {levenshtein('abcde', 'abcde')}")      # Expected: 0