"""Utility for counting overlapping occurrences of a substring.

The standard :py:meth:`str.count` method does **not** count overlapping
matches – e.g. ``'aaaa'.count('aa')`` returns ``2``.  This module provides a
single function :func:`count_overlapping` that returns the number of *overlapping*
occurrences.

Examples
--------
>>> count_overlapping('aaaa', 'aa')
3
>>> count_overlapping('abababa', 'aba')
3
>>> count_overlapping('abc', '')
0

The implementation uses the fast C‑level ``str.find`` in a loop, advancing the
search start by one character after each match.  This gives O(n) behaviour for
most inputs and avoids the quadratic cost of naïve slicing.
"""

from __future__ import annotations


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of *overlapping* occurrences of ``needle`` in ``haystack``.

    Parameters
    ----------
    haystack: str
        The string to be searched.
    needle: str
        The substring to look for.  An empty ``needle`` yields ``0`` by
        definition – counting empty matches would be ambiguous.

    Returns
    -------
    int
        Number of overlapping occurrences.
    """
    if not needle:
        return 0
    count = 0
    start = 0
    needle_len = len(needle)
    # Using str.find which is implemented in C and therefore fast.
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        # Advance by one to allow overlapping matches.
        start = idx + 1
        # Small optimisation: if remaining characters are fewer than needle,
        # we can stop early.
        if start > len(haystack) - needle_len:
            # No further full matches possible.
            break
    return count

__all__ = ["count_overlapping"]
