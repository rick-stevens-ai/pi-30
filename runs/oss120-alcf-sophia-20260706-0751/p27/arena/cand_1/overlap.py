# overlap.py
"""Utility to count overlapping substrings.

The function :func:`count_overlapping` returns the number of (potentially
overlapping) occurrences of *needle* within *haystack*.

Examples
--------
>>> count_overlapping('aaaa', 'aa')
3
>>> count_overlapping('abababa', 'aba')
3
>>> count_overlapping('abc', '')
0

The implementation uses :meth:`str.find` and advances the search start by
one character after each match, guaranteeing overlapping matches are
counted.  It runs in O(n) time for typical patterns and falls back to the
same complexity as ``str.find`` for pathological cases.
"""

from __future__ import annotations


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of overlapping occurrences of *needle* in *haystack*.

    Parameters
    ----------
    haystack: str
        The string to be searched.
    needle: str
        The substring to look for.  An empty needle yields ``0`` as per the
        specification.

    Returns
    -------
    int
        Count of (potentially overlapping) matches.
    """
    if not needle:
        return 0

    count = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        # Advance by one to allow overlapping matches
        start = idx + 1
    return count


__all__ = ["count_overlapping"]
