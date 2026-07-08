"""Utility for counting overlapping substrings.

The function :func:`count_overlapping` returns the number of (possibly overlapping)
occurrences of *needle* in *haystack*.

Examples
--------
>>> count_overlapping('aaaa', 'aa')
3
>>> count_overlapping('abababa', 'aba')
2
>>> count_overlapping('abc', '')
0

The implementation uses :str:`find` in a loop, advancing the search start by one
character after each match. This leverages the highly‑optimised C implementation
of ``str.find`` while correctly handling overlapping matches. The function
returns ``0`` for an empty needle, matching the conventional definition that an
empty pattern does not occur in a string.

Only the Python standard library is used.
"""

from __future__ import annotations

__all__ = ["count_overlapping"]


def count_overlapping(haystack: str, needle: str) -> int:
    """Count overlapping occurrences of *needle* in *haystack*.

    Parameters
    ----------
    haystack: str
        The string to be searched.
    needle: str
        The substring to count. An empty ``needle`` yields ``0``.

    Returns
    -------
    int
        Number of (possibly overlapping) occurrences of ``needle``.
    """
    if not needle:
        return 0

    count = 0
    start = 0
    # ``str.find`` is implemented in C and is very fast. After each match we
    # continue searching from the next character to allow overlapping matches.
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        # Move start one character after the current match start to allow overlap.
        start = idx + 1
    return count
