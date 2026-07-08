def levenshtein(a: str, b: str) -> int:
    """
    Computes the Levenshtein distance between two strings a and b.
    Uses a two-row dynamic programming approach with space optimization
    and common prefix/suffix trimming for performance.
    """
    if a == b:
        return 0

    n = len(a)
    m = len(b)

    # Early exit if one string is empty
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
        n = len(a)
        m = len(b)

    # Trim common suffix
    end_a = n - 1
    end_b = m - 1
    while end_a >= 0 and end_b >= 0 and a[end_a] == b[end_b]:
        end_a -= 1
        end_b -= 1

    if end_a < n - 1:
        a = a[:end_a + 1]
        b = b[:end_b + 1]
        n = len(a)
        m = len(b)

    # After trimming, check if any string is empty
    if n == 0:
        return m
    if m == 0:
        return n

    # Ensure 'a' is the shorter string to minimize space complexity
    if n > m:
        a, b = b, a
        n, m = m, n

    # Two-row DP implementation
    # prev_row represents dp[i-1], curr_row represents dp[i]
    prev_row = list(range(m + 1))
    curr_row = [0] * (m + 1)

    for i in range(1, n + 1):
        curr_row[0] = i
        char_a = a[i - 1]
        # Pre-fetch references if possible, but Python is tricky here.
        # The loop below is the hottest part of the code.
        for j in range(1, m + 1):
            cost = 0 if char_a == b[j - 1] else 1
            
            # Compute min of insertion, deletion, substitution
            sub = prev_row[j - 1] + cost
            ins = curr_row[j - 1] + 1
            dele = prev_row[j] + 1
            
            if sub <= ins and sub <= dele:
                curr_row[j] = sub
            elif ins <= dele:
                curr_row[j] = ins
            else:
                curr_row[j] = dele
            
        # Swap rows for next iteration (pointer swap is fast)
        prev_row, curr_row = curr_row, prev_row

    return prev_row[m]
