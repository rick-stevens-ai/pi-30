def levenshtein(a: str, b: str) -> int:
    """
    Computes the Levenshtein distance between two strings.
    Optimized with common prefix/suffix trimming and two-row DP.
    """
    # Trim common prefix
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    if i > 0:
        a = a[i:]
        b = b[i:]

    # Trim common suffix
    i = 0
    while i < len(a) and i < len(b) and a[-(i + 1)] == b[-(i + 1)]:
        i += 1
    if i > 0:
        a = a[:-i]
        b = b[:-i]

    n, m = len(a), len(b)
    if n == 0: return m
    if m == 0: return n

    # Ensure 'a' is the shorter string to minimize space complexity
    if n > m:
        a, b = b, a
        n, m = m, n

    # Current and previous rows of the DP table
    prev_row = list(range(n + 1))
    curr_row = [0] * (n + 1)

    for i in range(1, m + 1):
        curr_row[0] = i
        char_b = b[i - 1]
        for j in range(1, n + 1):
            # Cost is 0 if characters match, otherwise 1
            cost = 0 if a[j - 1] == char_b else 1
            
            # Min of: deletion, insertion, substitution
            curr_row[j] = min(
                prev_row[j] + 1,      # Deletion from b (or insertion into a)
                curr_row[j - 1] + 1,  # Insertion into b (or deletion from a)
                prev_row[j - 1] + cost # Substitution
            )
        # Swap rows: prev_row becomes curr_row for next iteration
        prev_row[:] = curr_row

    return prev_row[n]
