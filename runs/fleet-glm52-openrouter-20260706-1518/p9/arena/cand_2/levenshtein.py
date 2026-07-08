"""Levenshtein edit distance (two-row DP with early exits)."""

from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between strings *a* and *b*.

    Uses O(min(len(a), len(b))) memory via two rolling rows, with early
    termination when a common prefix/suffix exists and fast exits for the
    trivial length cases.
    """
    la = len(a)
    lb = len(b)

    # Fast paths for empty inputs.
    if la == 0:
        return lb
    if lb == 0:
        return la

    # Keep a as the shorter string so the rows are as narrow as possible.
    if lb < la:
        a, b = b, a
        la, lb = lb, la

    # Strip common prefix: those characters cost nothing and never affect
    # the distance for the remainder.
    start = 0
    while start < la and a[start] == b[start]:
        start += 1
    if start == la:
        # a is a prefix of b (or equal); remaining tail of b is the cost.
        return lb - start

    # Strip common suffix, being careful not to overlap the prefix.
    end_a = la - 1
    end_b = lb - 1
    while end_a >= start and end_b >= start and a[end_a] == b[end_b]:
        end_a -= 1
        end_b -= 1

    # Effective slices that actually need DP.
    a = a[start:end_a + 1]
    b = b[start:end_b + 1]
    m = len(a)
    n = len(b)

    if m == 0:
        return n
    if n == 0:
        return m

    # Two rolling rows. prev holds row i-1, curr holds row i.
    # prev[j] = distance between a[:i] and b[:j].
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        ai = a[i - 1]
        for j in range(1, n + 1):
            cost = 0 if ai == b[j - 1] else 1
            sub = prev[j - 1] + cost
            ins = curr[j - 1] + 1
            dele = prev[j] + 1
            v = sub if sub < ins else ins
            if dele < v:
                v = dele
            curr[j] = v
        prev, curr = curr, prev

    return prev[n]
