def levenshtein(a: str, b: str) -> int:
    """
    Compute the Levenshtein distance between two strings.
    
    Uses a space-optimized (two-row) dynamic programming approach.
    Time complexity: O(m*n), Space complexity: O(min(m, n)).
    """
    if a == b:
        return 0

    # Ensure b is the shorter string to minimize space usage
    if len(a) < len(b):
        a, b = b, a

    n, m = len(a), len(b)
    if m == 0:
        return n

    # prev_row represents the distances for the previous character of a
    prev_row = list(range(m + 1))
    # curr_row will store the distances for the current character of a
    curr_row = [0] * (m + 1)

    for i in range(1, n + 1):
        curr_row[0] = i
        char_a = a[i - 1]
        for j in range(1, m + 1):
            if char_a == b[j - 1]:
                curr_row[j] = prev_row[j - 1]
            else:
                # min of (deletion, insertion, substitution)
                # We use a nested if/min to avoid extra function calls
                m1 = prev_row[j]     # deletion
                m2 = curr_row[j - 1] # insertion
                m3 = prev_row[j - 1] # substitution
                
                if m1 < m2:
                    curr_row[j] = (m1 if m1 < m3 else m3) + 1
                else:
                    curr_row[j] = (m2 if m2 < m3 else m3) + 1
        
        # Copy curr_row to prev_row for the next iteration
        prev_row[:] = curr_row

    return prev_row[m]

if __name__ == "__main__":
    # Simple tests
    assert levenshtein("", "") == 0
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("flaw", "lawn") == 2
    assert levenshtein("a", "b") == 1
    assert levenshtein("", "abc") == 3
    print("Tests passed!")
