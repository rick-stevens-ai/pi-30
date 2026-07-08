def levenshtein(a, b):
    """
    Computes the Levenshtein edit distance between two strings.
    Optimized with common prefix/suffix trimming and space-efficient DP.
    """
    # Early exit for identity or empty strings
    if a == b:
        return 0
    
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n

    # Distinct Angle: Trim common prefix and suffix to reduce DP matrix size.
    # This significantly speeds up the process for similar strings.
    start = 0
    while start < n and start < m and a[start] == b[start]:
        start += 1
    
    end_a, end_b = n - 1, m - 1
    while end_a >= start and end_b >= start and a[end_a] == b[end_b]:
        end_a -= 1
        end_b -= 1

    # Slice the strings to work only on the differing middle part
    a = a[start : end_a + 1]
    b = b[start : end_b + 1]
    
    n, m = len(a), len(b)

    if n == 0:
        return m
    if m == 0:
        return n

    # Ensure 'a' is the shorter string to minimize space complexity O(min(n, m))
    if n > m:
        a, b = b, a
        n, m = m, n

    # Two-row DP implementation (using one row and a temporary variable for the diagonal)
    # This is functionally equivalent to two rows but slightly more memory efficient.
    current_row = list(range(n + 1))
    
    for i in range(1, m + 1):
        char_b = b[i - 1]
        prev_diag = current_row[0]
        current_row[0] = i
        
        for j in range(1, n + 1):
            prev_val = current_row[j]
            # Cost is 0 if characters match, otherwise 1
            cost = 0 if a[j - 1] == char_b else 1
            
            # Min of: deletion, insertion, substitution
            current_row[j] = min(
                current_row[j] + 1,      # deletion from b (or insertion into a)
                current_row[j - 1] + 1,  # insertion into b (or deletion from a)
                prev_diag + cost         # substitution
            )
            prev_diag = prev_val

    return current_row[n]

if __name__ == "__main__":
    # Basic tests
    test_cases = [
        ("kitten", "sitting", 3),
        ("flaw", "lawn", 2),
        ("", "", 0),
        ("abc", "", 3),
        ("", "abc", 3),
        ("equal", "equal", 0),
        ("intention", "execution", 5),
        ("a" * 100, "a" * 100, 0),
        ("a" * 100, "b" * 100, 100),
    ]
    for a, b, expected in test_cases:
        result = levenshtein(a, b)
        assert result == expected, f"Failed on {a}, {b}: expected {expected}, got {result}"
    print("All tests passed!")
