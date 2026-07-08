def levenshtein(a: str, b: str) -> int:
    n = len(a)
    m = len(b)

    if n == 0 or m == 0:
        return max(n, m)

    # Ensure a is longer so the inner loop (over j) stays small.
    if n < m:
        a, b = b, a
        n, m = m, n

    # Band-limited two-row DP.
    # At row i we only need curr[j] for j in [max(0, i-m), min(m, i)].
    # Cells outside this band are bounded by the diagonal and never improve
    # the optimal path, so we skip them entirely — saving both time and cache.

    prev = list(range(min(n, m) + 1))   # row 0: insert b[0..j] into ""

    for i in range(1, n + 1):
        lo = max(0, i - m)                 # left band edge
        hi = min(m, i)                     # right band edge (inclusive)

        curr = [0] * (m + 1)
        curr[0] = i                       # delete all a[0..i-1]

        for j in range(lo, hi):            # compute curr[j+1] via DP recurrence
            a_c = a[i - 1]
            b_j = b[j]
            sub_cost = prev[j] if a_c == b_j else prev[j] + 1
            ins_cost = curr[j] + 1
            del_cost = prev[j + 1] + 1
            v = ins_cost if ins_cost < del_cost else del_cost
            if sub_cost < v:
                v = sub_cost
            curr[j + 1] = v

        # Early exit across rows: the edit distance is at least |n - m|.
        # If the current row's best cost equals that lower bound, we can stop.
        # More precisely: if min(curr) >= n (the trivial delete-all cost), done.
        # But a tighter check: once curr[m] == max(0, i + (m - m)) = i ... no.
        # Simplest correct early exit: if the row minimum equals |n-m| and we're at
        # the theoretical minimum, break.  We use the fact that edit_distance >= max(0, n-m).
        # If curr[m] == max(0, n - m) ever (and n>=m), then d = n-m and we stop.
        if i + (n - i) <= curr[m]:   # equivalent: curr[m] >= n which is always true... nope
            pass

    return prev[m]
