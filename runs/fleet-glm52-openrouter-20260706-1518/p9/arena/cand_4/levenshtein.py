"""Levenshtein edit distance - two-row DP with prefix/suffix trimming and early exits."""

from __future__ import annotations


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between strings a and b.

    Edit operations: insertion, deletion, substitution (unit cost each).
    Uses two-row dynamic programming with O(min(len)) memory, plus
    prefix/suffix trimming and a fast-path when one string is empty or a
    prefix of the other.
    """
    la, lb = len(a), len(b)

    # Empty-string fast paths.
    if la == 0:
        return lb
    if lb == 0:
        return la

    # Make `a` the shorter string so the DP row width (len(b)+1) is smaller.
    if lb < la:
        a, b = b, a
        la, lb = lb, la

    # Trim common prefix. These characters match at no cost.
    start = 0
    while start < la and a[start] == b[start]:
        start += 1
    # If all of the (shorter) `a` matched as a prefix, the remaining tail of
    # `b` is the only cost: pure insertions/deletions of length (lb - la).
    if start == la:
        return lb - la

    # Trim common suffix (beyond the shared prefix region).
    end = 0
    while end < la - start and a[la - 1 - end] == b[lb - 1 - end]:
        end += 1

    a = a[start: la - end]
    b = b[start: lb - end]
    la -= start + end
    lb -= start + end

    # After trimming, re-check empties (suffix trim may have emptied a side).
    if la == 0:
        return lb
    if lb == 0:
        return la

    # Two rolling rows: prev holds distances for a[:i-1] vs b[:*],
    # cur holds distances for a[:i] vs b[:*].
    prev = list(range(lb + 1))
    cur = [0] * (lb + 1)

    # Hoist attribute/element lookups for speed in the inner loop.
    b_local = b

    for i in range(1, la + 1):
        ca = a[i - 1]
        # j = 0 cell: distance between a[:i] and "" is i (i deletions).
        cur[0] = i
        row_min = i
        for j in range(1, lb + 1):
            # cost = 0 if current chars equal else 1
            cost = 0 if ca == b_local[j - 1] else 1
            d = prev[j - 1] + cost          # substitution / match
            ins = cur[j - 1] + 1            # insertion into b
            if ins < d:
                d = ins
            dele = prev[j] + 1              # deletion from a
            if dele < d:
                d = dele
            cur[j] = d
            if d < row_min:
                row_min = d
        prev, cur = cur, prev

    return prev[lb]


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if len(args) == 2:
        print(levenshtein(args[0], args[1]))
    else:
        # Sanity checks.
        assert levenshtein("", "") == 0
        assert levenshtein("", "abc") == 3
        assert levenshtein("abc", "") == 3
        assert levenshtein("kitten", "sitting") == 3
        assert levenshtein("flaw", "lawn") == 2
        assert levenshtein("same", "same") == 0
        assert levenshtein("a", "b") == 1
        assert levenshtein("ab", "xyzAB") == 5
        assert levenshtein("abc", "yabc") == 1
        assert levenshtein("xabcy", "abc") == 2
        print("ok")
