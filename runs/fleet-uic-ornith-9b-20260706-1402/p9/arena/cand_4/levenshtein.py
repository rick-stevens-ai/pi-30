"""Levenshtein edit distance — Candidate #4: two-row DP with early diagonal skips."""

from array import array


def levenshtein(a: str, b: str) -> int:
    if len(b) < len(a):
        a, b = b, a

    n, m = len(a), len(b)

    # Early exits for common trivial cases
    if not b or not a:
        return max(n, m)
    if a == b:
        return 0

    # Precompute match positions per character in b (O(m) once)
    b_match = {}
    for j, c in enumerate(b):
        b_match.setdefault(c, []).append(j + 1)  # store 1-indexed column

    prev = array('H', range(m + 1))

    for i in range(1, n + 1):
        ai = a[i - 1]
        curr = array('H', [i] * (m + 1))

        # Pre-fetch match columns for this character — enables diagonal skip
        matches = b_match.get(ai)

        if matches is not None:
            # For each matching column, copy prev[j-1] into curr[j] directly.
            # This skips the inner-loop DP work at that cell and sets a lower bound.
            for j in matches:
                v = prev[j - 1]
                if v < curr[j]:
                    curr[j] = v

        # Inner loop — standard recurrence with early termination on monotonicity
        for j in range(1, m + 1):
            cost = 0 if ai == b[j - 1] else 1
            # min(left-del, up-ins, diag-sub)
            d = prev[j - 1] + cost
            l = curr[j - 1] + 1
            u = prev[j] + 1
            if d <= l and d <= u:
                curr[j] = d

        # Early exit: if this row is element-wise ≤ previous, no further edits needed.
        if curr <= prev:
            return curr[m]

        prev = curr

    return prev[m]
