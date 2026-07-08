def levenshtein(a: str, b: str) -> int:
    \"\"\"Return the Levenshtein edit distance between strings a and b.

    Works for empty inputs and uses a two‑row dynamic programming approach
    with O(min(len(a), len(b))) extra space. An early return is used when the
    strings are equal.
    \"\"\"
    if a == b:
        return 0
    m, n = len(a), len(b)
    if m == 0:
        return n
    if n == 0:
        return m

    # Ensure the inner loop iterates over the shorter string to reduce memory usage
    if m < n:
        a, b = b, a
        m, n = n, m

    previous = list(range(n + 1))
    for i in range(1, m + 1):
        current = [i]                     # cost of deletions to reach empty prefix of b
        ai = a[i - 1]
        for j in range(1, n + 1):
            cost = 0 if ai == b[j - 1] else 1
            deletion = previous[j] + 1          # dp[i-1][j] + 1
            insertion = current[j - 1] + 1      # dp[i][j-1] + 1
            substitution = previous[j - 1] + cost
            current.append(min(deletion, insertion, substitution))
        previous = current

    return previous[n]