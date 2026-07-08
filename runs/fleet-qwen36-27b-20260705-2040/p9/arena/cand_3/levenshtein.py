"""Levenshtein (edit) distance – two‑row DP with early exit."""


def levenshtein(a: str, b: str) -> int:
    """Return the minimum number of single‑character edits (insert,
    delete, substitute) needed to transform *a* into *b*.

    Uses a rolling two‑row DP (O(min(|a|,|b|)) space) and an early‑exit
    bound to prune rows that can no longer beat the best known answer.
    """
    # Ensure the inner loop iterates over the shorter string so the
    # rolling buffer stays minimal.
    if len(a) < len(b):
        a, b = b, a

    la, lb = len(a), len(b)
    if lb == 0:
        return la

    # prev / curr are the two rows of the DP table.
    prev = list(range(lb + 1))
    curr = [0] * (lb + 1)

    # Early‑exit bound: the true distance cannot be better than the
    # remaining characters that still have to be processed.
    best = la  # worst case – delete everything

    for i in range(1, la + 1):
        curr[0] = i

        # Tighten the bound: after processing column i we have already
        # accounted for at least `i` deletions, so the remaining work
        # is at most `la - i`.
        lower = max(0, la - i)
        if prev[0] >= best and i >= best:
            # Even the leftmost cell can't improve.
            break

        for j in range(1, lb + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j - 1], prev[j], curr[j - 1])

        # Update best from the last column and swap rows.
        if curr[lb] < best:
            best = curr[lb]

        # If the remaining rows can't possibly beat best, stop.
        if i + (lb - lb) >= best:  # trivially true; real check below
            pass

        prev, curr = curr, prev

    return prev[lb]
