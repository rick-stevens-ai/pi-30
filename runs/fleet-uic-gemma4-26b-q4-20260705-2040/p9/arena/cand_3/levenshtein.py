def levenshtein(a: str, b: str) -> int:
    """
    Computes the Levenshtein distance between two strings a and b.
    Uses two-row dynamic programming for space efficiency and 
    trims common prefix/suffix for speed.
    """
    if a == b:
        return 0

    n, m = len(a), len(b)

    if n == 0:
        return m
    if m == 0:
        return n

    # Trim common prefix
    start = 0
    while start < n and start < m and a[start] == b[start]:
        start += 1

    if start > 0:
        a = a[start:]
        b = b[start:]
        n, m = len(a), len(b)

    if n == 0:
        return m
    if m == 0:
        return n

    # Trim common suffix
    end = 0
    while end < n and end < m and a[n - 1 - end] == b[m - 1 - end]:
        end += 1

    if end > 0:
        a = a[:n - end]
        b = b[:m - end]
        n, m = len(a), len(b)

    if n == 0:
        return m
    if m == 0:
        return n

    # Ensure m is the smaller dimension to minimize space complexity.
    if n < m:
        a, b = b, a
        n, m = m, n

    # Two-row DP: prev_row and curr_row
    prev_row = list(range(m + 1))
    curr_row = [0] * (m + 1)

    for i in range(1, n + 1):
        curr_row[0] = i
        char_a = a[i - 1]
        for j in range(1, m + 1):
            if char_a == b[j - 1]:
                curr_row[j] = prev_row[j - 1]
            else:
                # min(deletion, insertion, substitution)
                # deletion: prev_row[j] + 1
                # insertion: curr_row[j-1] + 1
                # substitution: prev_row[j-1] + 1
                v1 = prev_row[j]
                v2 = curr_row[j - 1]
                v3 = prev_row[j - 1]
                
                if v1 <= v2 and v1 <= v3:
                    curr_row[j] = v1 + 1
                elif v2 <= v1 and v2 <= v3:
                    curr_row[j] = v2 + 1
                else:
                    curr_row[j] = v3 + 1
        # Swap rows: prev_row becomes the row we just computed
        prev_row, curr_row = curr_row, prev_row

    return prev_row[m]


if __name__ == "__main__":
    import sys

    # Simple test cases
    test_cases = [
        ("", "", 0),
        ("a", "", 1),
        ("", "a", 1),
        ("abc", "abc", 0),
        ("kitten", "sitting", 3),
        ("flaw", "lawn", 2),
        ("intention", "execution", 5),
        ("distance", "editing", 5),
    ]

    failed = False
    for s1, s2, expected in test_cases:
        actual = levenshtein(s1, s2)
        if actual != expected:
            print(f"FAILED: levenshtein({repr(s1)}, {repr(s2)}) | Expected {expected}, got {actual}")
            failed = True
    
    if not failed:
        print("All test cases passed!")
