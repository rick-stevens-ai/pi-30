def levenshtein(a: str, b: str) -> int:
    """
    Calculates the Levenshtein distance between two strings a and b.

    Uses a two-row dynamic programming approach for space efficiency.
    """
    if len(a) < len(b):
        # Ensure 'a' is the longer string to potentially optimize space if we swap,
        # but for simplicity, let's just ensure the smaller dimension dictates the row size.
        a, b = b, a

    m = len(a)
    n = len(b)

    if m == 0:
        return n
    if n == 0:
        return m

    # Initialize the first row (distance from empty string to prefixes of b)
    # dp_prev[j] will store the distance between a[:i-1] and b[:j]
    dp_prev = list(range(n + 1))

    for i in range(1, m + 1):
        # Initialize the current row's first element (distance from a[:i] to empty string)
        dp_curr = [i] * (n + 1)
        
        # Optimization: Keep track of the minimum distance found in the current row
        min_dist = float('inf')

        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            
            # Calculate the three possible operations:
            # 1. Deletion: dp_prev[j] + 1 (from previous row, same column)
            # 2. Insertion: dp_curr[j-1] + 1 (from current row, previous column)
            # 3. Substitution: dp_prev[j-1] + cost (from previous row, previous column)
            
            dp_curr[j] = min(
                dp_prev[j] + 1,        # Deletion from a
                dp_curr[j - 1] + 1,    # Insertion into a (or deletion from b)
                dp_prev[j - 1] + cost  # Substitution/Match
            )
            
            if dp_curr[j] < min_dist:
                min_dist = dp_curr[j]

        dp_prev = dp_curr

    return dp_prev[n]

if __name__ == '__main__':
    # Test cases
    print(f"levenshtein('', 'abc'): {levenshtein('', 'abc')}") # Expected: 3
    print(f"levenshtein('kitten', 'sitting'): {levenshtein('kitten', 'sitting')}") # Expected: 3
    print(f"levenshtein('flaw', 'lawn'): {levenshtein('flaw', 'lawn')}") # Expected: 2
    print(f"levenshtein('', ''): {levenshtein('', '')}") # Expected: 0
    print(f"levenshtein('abc', ''): {levenshtein('abc', '')}") # Expected: 3
    print(f"levenshtein('a', 'a'): {levenshtein('a', 'a')}") # Expected: 0
    print(f"levenshtein('a', 'b'): {levenshtein('a', 'b')}") # Expected: 1