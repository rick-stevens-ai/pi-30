# overlap.py
"""Utility to count overlapping occurrences of a substring.

The standard ``str.count`` does **not** count overlapping matches::

    >>> 'aaaa'.count('aa')
    2

Our ``count_overlapping`` returns 3 for that example, because the matches
can start at positions 0, 1 and 2.

The implementation is deliberately lightweight and fast for long strings:
* it falls back to a simple loop using ``str.find`` that advances the start
  index by one after each match.
* for an empty ``needle`` the result is defined as ``0`` (consistent with
  ``str.count`` behaviour for empty patterns).
* only the Python standard library is used.
"""

from __future__ import annotations

__all__ = ["count_overlapping"]


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of **overlapping** occurrences of ``needle`` in ``haystack``.

    Args:
        haystack: The string to be searched.
        needle:   The substring to look for. An empty ``needle`` returns ``0``.

    Returns:
        The count of overlapping matches.

    Examples
    --------
    >>> count_overlapping('aaaa', 'aa')
    3
    >>> count_overlapping('abababa', 'aba')
    3
    >>> count_overlapping('abc', '')
    0
    """
    # Edge case – an empty substring would match at every position, but the
    # convention for this utility (and for ``str.count``) is to treat it as
    # having zero matches.
    if not needle:
        return 0

    count = 0
    start = 0
    needle_len = len(needle)
    # ``str.find`` is implemented in C and is highly optimized. By moving the
    # start index only one character past the previous match we ensure that
    # overlapping occurrences are captured.
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        # Advance by one to allow overlapping matches.
        start = idx + 1
        # Small optimisation: if the remaining part of the haystack is shorter
        # than ``needle`` we can stop early.
        if len(haystack) - start < needle_len:
            break
    return count
