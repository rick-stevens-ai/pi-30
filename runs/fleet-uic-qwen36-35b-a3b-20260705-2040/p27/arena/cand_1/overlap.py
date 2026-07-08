"""Overlapping substring occurrence counter — KMP (Knuth-Morris-Pratt) engine.

O(n + m) time, O(m) space. Handles empty needle → 0 immediately.
Uses the classic failure-function approach so every valid starting pos in
haystack is visited exactly once — no backtracking, full overlap support."""


def count_overlapping(haystack: str, needle: str) -> int:
    if not needle:                     # empty target has zero matches
        return 0

    m = len(needle)
    n = len(haystack)
    if m > n:
        return 0

    # ── Build KMP failure (partial-match) table ──
    fail = [0] * m                     # fails[i] = longest proper-prefix of needle[:i+1]
                                       #              that is also a suffix of needle[:i+1]
    j = 0                              # length of previous longest prefix-suffix
    for i in range(1, m):
        while j and needle[i] != needle[j]:
            j = fail[j - 1]
        if needle[i] == needle[j]:
            j += 1
        fail[i] = j

    # ── Scan haystack with KMP automaton ──
    count = 0
    j = 0                              # current match length in needle
    for i in range(n):
        while j and haystack[i] != needle[j]:
            j = fail[j - 1]
        if haystack[i] == needle[j]:
            j += 1

        if j == m:                     # full match ending at position i
            count += 1
            j = fail[m - 1]            # allow overlap — slide to longest proper prefix that's also suffix

    return count
