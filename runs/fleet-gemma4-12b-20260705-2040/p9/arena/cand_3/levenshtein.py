def levenshtein(a: str, b: str) -> int:
    """
    Compute the Levenshtein distance between two strings a and b.
    
    The Levenshtein distance is the minimum number of single-character edits 
    (insertions, deletions, or substitutions) required to transform one 
    string into the other.

    This implementation uses a space-optimized dynamic programming approach 
    with O(min(m, n)) space complexity and O(m*n) time complexity.
    """
    if a == b:
        return 0
    
    m, n = len(a), len(b)
    if m == 0:
        return n
    if n == 0:
        return m

    # Ensure that the second string is the shorter one to minimize space usage.
    if m < n:
        a, b = b, a
        m, n = n, m

    # dp array stores the distances for the current row.
    # We only need one row of size (min(m, n) + 1).
    dp = list(range(n + 1))

    for i in range(1, m + 1):
        prev_diag = dp[0]
        dp[0] = i
        char_a = a[i-1]
        for j in range(1, n + 1):
            # prev_diag is the value of dp[i-1][j-1]
            # dp[j] is the value of dp[i-1][j] (before update)
            # dp[j-1] is the value of dp[i][j-1] (already updated)
            
            temp = dp[j]
            cost = 0 if char_a == b[j-1] else 1
            
            # min(deletion, insertion, substitution)
            res = dp[j] + 1
            if dp[j-1] + 1 < res:
                res = dp[j-1] + 1
            if prev_diag + cost < res:
                res = prev_diag + cost
            
            dp[j] = res
            prev_diag = temp

    return dp[n]

if __name__ == "__main__":
    # Basic tests
    assert levenshtein("", "") == 0
    assert levenshtein("kitten", "sit") == 3
    assert levenshtein("flaw", "lawn") == 2
    assert levenshtein("geeks", "geeks") == 0
    assert levenshtein("a", "") == 1
    assert levenshtein("", "a") == 1
    print("All tests passed!")
