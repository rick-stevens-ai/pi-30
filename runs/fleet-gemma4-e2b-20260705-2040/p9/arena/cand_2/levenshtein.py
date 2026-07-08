def levenshtein(a: str, b: str) -> int:
    """
    Calculates the Levenshtein distance (edit distance) between two strings a and b.

    Uses a space-optimized two-row dynamic programming approach for efficiency.

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

    # Ensure the shorter string is used for the dimension of the DP array (for space optimization)
    if len_a < len_b:
        # Swap a and b so that 'a' is always the longer or equal length string
        a, b = b, a
        len_a, len_b = len_b, len_a

    # Initialize the previous row (dp array)
    # dp[j] will hold the distance between a[:i] and b[:j]
    previous_row = list(range(len_b + 1))

    for i in range(1, len_a + 1):
        current_row = [i]
        # Optimization: Calculate the minimum cost for the first column (deletion from a)
        # The distance between a[:i] and an empty string b[:0] is i.
        current_row[0] = i

        for j in range(1, len_b + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            # Calculate the three possibilities:
            # 1. Deletion: previous_row[j] + 1 (deletion from a)
            # 2. Insertion: current_row[-1] + 1 (insertion into a, corresponds to b[j-1])
            # 3. Substitution: previous_row[j - 1] + cost (substitution/match)
            
            insertion = current_row[j - 1] + 1
            deletion = previous_row[j] + 1
            substitution = previous_row[j - 1] + cost

            current_row.append(min(insertion, deletion, substitution))

        previous_row = current_row

    # The result is the last element of the final row computed
    return previous_row[len_b]

if __name__ == '__main__':
    # Test cases
    print(f"levenshtein('kitten', 'sitting'): {levenshtein('kitten', 'sitting')}") # Expected: 3
    print(f"levenshtein('flaw', 'lawn'): {levenshtein('flaw', 'lawn')}")         # Expected: 2
    print(f"levenshtein('', 'abc'): {levenshtein('', 'abc')}")                 # Expected: 3
    print(f"levenshtein('abc', ''): {levenshtein('abc', '')}")                 # Expected: 3
    print(f"levenshtein('abc', 'abc'): {levenshtein('abc', 'abc')}")           # Expected: 0
    print(f"levenshtein('', ''): {levenshtein('', '')}")                       # Expected: 0
    print(f"levenshtein('a', 'b'): {levenshtein('a', 'b')}")                   # Expected: 1
    print(f"levenshtein('a', 'a'): {levenshtein('a', 'a')}")                   # Expected: 0