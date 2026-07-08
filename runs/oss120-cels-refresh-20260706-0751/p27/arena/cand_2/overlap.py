"""Utility for counting overlapping substrings.

The standard :py:meth:`str.count` does **not** count overlapping
occurrences – e.g. ``'aa'`` occurs three times in ``'aaaa'`` when overlaps
are allowed.  This module provides :func:`count_overlapping` which returns
the number of *overlapping* occurrences of ``needle`` in ``haystack``.

The implementation uses a zero‑width positive look‑ahead regular expression
(``(?=…)``) which scans the string in linear time and works correctly for
any Unicode pattern.  An empty ``needle`` is defined to have zero matches
(equivalent to the behaviour of many standard libraries).

Only the Python standard library is used.
"""

from __future__ import annotations

import re
from typing import Final

__all__: Final = ["count_overlapping"]


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of *overlapping* occurrences of ``needle`` in ``haystack``.

    Parameters
    ----------
    haystack:
        The string to be searched.
    needle:
        The substring to look for.  An empty ``needle`` yields ``0``.

    Returns
    -------
    int
        The count of overlapping matches.

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
        # By definition we treat an empty pattern as having no matches.
        return 0

    # ``(?=needle)`` is a zero‑width assertion that succeeds at every
    # position where ``needle`` starts. ``re.escape`` guarantees that any
    # characters in ``needle`` are interpreted literally.
    pattern = re.compile(r"(?={})".format(re.escape(needle)))
    # ``findall`` returns one entry per match because the pattern has zero
    # width – the actual match object is an empty string, but the count is
    # what we need.
    return len(pattern.findall(haystack))
