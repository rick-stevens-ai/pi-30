"""Utility for counting overlapping occurrences of a substring.

The standard :py:meth:`str.count` method does *not* count overlapping matches:

>>> 'aaaa'.count('aa')
2

For many text‑processing tasks we need the overlapping count, e.g. ``'aaaa'``
contains three overlapping occurrences of ``'aa'``::

    a a a a
    ^ ^ ^

This module provides :func:`count_overlapping` which implements that behaviour
using only the Python standard library and runs in linear time on typical
inputs.

The implementation uses :py:meth:`str.find` in a loop, advancing the search
position by **one** after each match.  ``str.find`` is a highly‑optimised C
function, so the overall algorithm is fast even for very long strings.

Edge cases:

* An empty ``needle`` yields ``0`` – counting empty substrings is undefined
  for this helper.
* If ``needle`` is longer than ``haystack`` the result is ``0``.
"""

from __future__ import annotations

__all__ = ["count_overlapping"]


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of **overlapping** occurrences of *needle* in *haystack*.

    Parameters
    ----------
    haystack: str
        The string to be searched.
    needle: str
        The substring to look for.  An empty needle returns ``0``.

    Returns
    -------
    int
        Count of overlapping matches.

    Examples
    --------
    >>> count_overlapping('aaaa', 'aa')
    3
    >>> count_overlapping('abababa', 'aba')
    2
    >>> count_overlapping('abc', '')
    0
    """
    if not needle:
        return 0

    count = 0
    start = 0
    # Using str.find is O(n) in C; we advance the start index by one to allow
    # overlapping matches.
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        # Move just one character forward to enable overlapping detection.
        start = idx + 1
    return count
