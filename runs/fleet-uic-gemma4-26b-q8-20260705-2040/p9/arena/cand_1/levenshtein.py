def levenshtein(a: str, b: str) -> int:
    """
    Calculates the Levenshtein distance between two strings.
    
    Uses a space-optimized (one-row) dynamic programming approach 
    with prefix and suffix trimming for early optimization.

    Complexity:
        Time: O(n * m)
        Space: O(min(n, m))
    """
    if a == b:
        return 0

    len_a = len(a)
    len_b = len(b)

    # Trim common prefix
    start = 0
    while start < len_a and start < len_b and a[start] == b[start]:
        start += 1

    if start > 0:
        a = a[start:]
        b = b[start:]
        len_a -= start
        len_b -= start

    # Trim common suffix
    end_a = len_a - 1
    end_b = len_b - 1
    while end_a >= 0 and end_b >= 0 and a[end_a] == b[end_b]:
        end_a -= 1
        end_b -= 1

    if end_a < len_a - 1 or end_b < len_b - 1:
        a = a[:end_a + 1]
        b = b[:end_b + 1]
        len_a = len(a)
        len_b = len(b)

    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure b is the shorter string to minimize space complexity to O(min(n, m))
    if len_a < len_b:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # dp array stores the current row's distances.
    dp = list(range(len_b + 1))

    for i in range(1, len_a + 1):
        pre_diagonal = dp[0]
        dp[0] = i
        char_a = a[i - 1]
        for j in range(1, len_b + 1):
            temp = dp[j]
            if char_a == b[j - 1]:
                dp[j] = pre_diagonal
            else:
                # min() is faster than manual if-else in Python for multiple arguments
                m_val = pre_diagonal
                if dp[j] < m_val: m_val = dp[j]
                if dp[j-1] < m_val: m_val = dp[j-1]
                dp[j] = m_val + 1
            pre_diagonal = temp

    return dp[len_b]

if __name__ == "__main__":
    # Quick test cases
    assert levenshtein("", "") == 0
    assert levenshtein("abc", "") == 3
    assert levenshtein("", "abc") == 3
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("flaw", "lawn") == 2
    assert levenshtein("intention", "execution") == 5
    assert levenshtein("abcde", "abcde") == 0
    assert levenshtein("abcde", "abfde") == 1
    print("All tests passed!")
