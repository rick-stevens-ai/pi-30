def levenshtein(a, b):
    """Levenshtein edit distance via two-row DP with prefix/suffix trim."""

    # Empty-input short-circuits
    if not a and not b:
        return 0
    if not a or not b:
        return max(len(a), len(b))

    n, m = len(a), len(b)

    # Always iterate over the longer string in the outer loop.
    # This makes the inner loop (over the shorter string's columns) as short
    # as possible and lets us detect row-equality early-exit cheaply.
    if m > n:
        a, b = b, a
        n, m = m, n

    # --- trim matching prefix & suffix before DP ---
    pfx = 0
    while pfx < n and pfx < m and a[pfx] == b[pfx]:
        pfx += 1
    sfx = 0
    while (sfx < n - pfx) and (sfx < m - pfx) \
            and a[n - 1 - sfx] == b[m - 1 - sfx]:
        sfx += 1

    if pfx + sfx >= min(n, m):
        return 0

    # --- two-row DP over the trimmed region ---
    prev = list(range(m + 1))          # row above current; column j holds dist(b[:j], a[:i])
    curr = [m] * (m + 1)              # pre-fill so first comparison uses correct value

    for i in range(pfx, n - sfx):
        c = curr[0] = i - pfx + 1      # cost of deleting all characters of a[pfx..i]

        for j in range(1, m + 1):
            if a[i - pfx] == b[j - 1]:
                curr[j] = prev[j - 1]
            else:
                v0 = prev[j]          # deletion from a
                v1 = c               # insertion into b (curr is the "left" row)
                v2 = prev[j - 1]     # substitution
                if v0 <= v1 and v0 <= v2:
                    curr[j] = v0 + 1
                elif v1 <= v2:
                    curr[j] = v1 + 1
                else:
                    curr[j] = v2 + 1

        prev, curr = curr, prev       # swap rows

    return prev[m]
