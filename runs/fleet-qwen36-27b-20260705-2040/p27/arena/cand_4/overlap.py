"""Count overlapping substring occurrences using KMP (Knuth-Morris-Pratt).

KMP preprocesses the needle into a failure table in O(m), then scans the
haystack in O(n) — never backtracking.  This gives guaranteed O(n + m)
time and O(m) extra space, which is optimal for the worst case.
"""

from __future__ import annotations


def _build_table(needle: str) -> list[int]:
    """Build the KMP failure (partial-match) table for *needle*.

    table[i] is the length of the longest proper prefix of needle[:i+1]
    that is also a suffix of needle[:i+1].
    """
    m = len(needle)
    table = [0] * m
    length = 0  # length of the previous longest prefix-suffix

    i = 1
    while i < m:
        if needle[i] == needle[length]:
            length += 1
            table[i] = length
            i += 1
        elif length:
            length = table[length - 1]
        else:
            table[i] = 0
            i += 1
    return table


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of *overlapping* occurrences of *needle* in *haystack*.

    Examples
    --------
    >>> count_overlapping("aaaa", "aa")
    3
    >>> count_overlapping("ababab", "abab")
    2
    >>> count_overlapping("hello", "")
    0
    >>> count_overlapping("abc", "abcd")
    0
    """
    if not needle:
        return 0

    n, m = len(haystack), len(needle)
    if m > n:
        return 0

    table = _build_table(needle)

    count = 0
    i = j = 0  # i indexes haystack, j indexes needle

    while i < n:
        if haystack[i] == needle[j]:
            i += 1
            j += 1

        if j == m:
            count += 1
            j = table[j - 1]  # continue searching from the longest prefix
        elif i < n and haystack[i] != needle[j]:
            if j:
                j = table[j - 1]
            else:
                i += 1

    return count
