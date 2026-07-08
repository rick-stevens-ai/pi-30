def levenshtein(a: str, b: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.
    Uses a space-optimized dynamic programming approach (O(min(m, n)) space).
    """
    if a == b:
        return 0

    # Ensure b is the shorter string to minimize space complexity
    if len(a) < len(b):
        a, b = b, a

    m, n = len(a), len(b)
    if n == 0:
        return m

    # dp[j] will store the edit distance between a[:i] and b[:j]
    dp = list(range(n + 1))

    for i in range(1, m + 1):
        prev_diag = dp[0]
        dp[0] = i
        char_a = a[i-1]
        for j in range(1, n + 1):
            temp = dp[j]
            cost = 0 if char_a == b[j-1] else 1
            
            # min(deletion, insertion, substitution)
            # dp[j] is the value from the previous row at index j (deletion)
            # dp[j-1] is the value from the current row at index j-1 (insertion)
            # prev_diag is the value from the previous row at index j-1 (substitution)
            
            res = dp[j] + 1
            if dp[j-1] + 1 < res:
                res = dp[j-1] + 1
            if prev_diag + cost < res:
                res = prev_diag + cost
            
            dp[j] = res
            prev_diag = temp

    return dp[n]

if __name__ == "__main__":
    # Test cases
    assert levenshtein("", "") == 0
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("flaw", "lawn") == 2
    assert levenshtein("a", "b") == 1
    assert levenshtein("abc", "") == 3
    assert levenshtein("", "abc") == 3
    print("All tests passed!")
