"""Count overlapping occurrences of needle in haystack via KMP prefix-function."""

from typing import List


def _build_prefix_table(pattern: str) -> List[int]:
    """Return the Knuth–Morris–Pratt failure (prefix) table for *pattern*.

    pi[i] = length of the longest proper prefix of pattern[0:i+1]
    that is also a suffix of pattern[0:i+1].
    """
    m = len(pattern)
    pi: List[int] = [0] * m
    k = 0  # length of previous longest prefix suffix
    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = pi[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        pi[i] = k
    return pi


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of **overlapping** occurrences of *needle* in *haystack*.

    Examples
    --------
    >>> count_overlapping('aaaa', 'aa')
    3
    >>> count_overlapping('ababab', 'abab')
    2
    >>> count_overlapping('hello', '')
    0

    Complexity: O(len(haystack) + len(needle)) time, O(len(needle)) space.
    """
    if not needle:
        return 0

    n, m = len(haystack), len(needle)
    if m > n:
        return 0

    pi = _build_prefix_table(needle)

    count = 0
    j = 0  # index into needle
    for i in range(n):
        while j > 0 and needle[j] != haystack[i]:
            j = pi[j - 1]
        if needle[j] == haystack[i]:
            j += 1
        if j == m:
            count += 1
            j = pi[j - 1]  # resume from the longest proper prefix that is also a suffix

    return count
