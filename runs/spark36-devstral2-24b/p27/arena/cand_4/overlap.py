#!/usr/bin/env python
"""
overlap.py - Fast overlapping substring counter.
Implements count_overlapping(haystack, needle) -> int
that counts all occurrences including overlapping ones (e.g., 'aa' in 'aaaa' is 3).
Also handles empty haystack or needle correctly (returning 0). Uses only stdlib.
Candidate #4 distinct implementation angle: Knuth-Morris-Pratt (KMP) algorithm adapted
to count overlapping matches via prefix function manipulation.
"""
from typing import List


def _build_prefix_function(pattern: str) -> List[int]:
    """Build KMP prefix function for pattern. Used to enable fast search and overlap counting."""
    n = len(pattern)
    if n == 0:
        return []
    pi = [0] * n
    k = 0
    for q in range(1, n):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
        pi[q] = k
    return pi


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count all occurrences of `needle` within `haystack`, including overlapping ones.

    Examples:
        count_overlapping('aaaa','aa') == 3
        count_overlapping('','') == 0
        count_overlapping('', 'x') == 0
        count_overlapping('abcabc', 'ab') == 2

    Strategy: Use KMP-style search. Instead of skipping len(needle)-pi[j] on non-match,
    we skip pi[j]-1 when a match would otherwise overlap, enabling overlapping
    matches to be counted correctly.
    """
    # Early exits
    if not haystack or not needle:
        return 0

    m, n = len(haystack), len(needle)
    pi = _build_prefix_function(needle)

    count = 0
    q: int = 0  # current position in text
    while q < m:
        if haystack[q] == needle[0]:
            # potential match at q; check full pattern
            k = 1
            r: int = q + 1
            while k < n and r < m and haystack[r] == needle[k]:
                k += 1
                r += 1
            if k == n:
                # match found starting at q
                count += 1
                q = r - pi[-1]
            else:
                q = r
        else:
            q += 1
    return count


# Small doctest for demonstration (no tests in deliverable)
def _test():
    assert count_overlapping('aaaa', 'aa') == 3, 'overlap: aa in aaaa'
    assert count_overlapping('', '') == 0, 'empty needle'
    assert count_overlapping('bbb', 'a') == 0, 'no match'
    print(' doctest passed')


if __name__ == '__main__':
    _test()
