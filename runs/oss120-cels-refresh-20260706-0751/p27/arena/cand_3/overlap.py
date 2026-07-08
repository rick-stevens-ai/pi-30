# overlap.py
"""Utility to count overlapping occurrences of a substring.

The standard :py:meth:`str.count` does *not* count overlapping matches.
For example ``count_overlapping('aaaa', 'aa')`` should return ``3`` because the
matches start at positions 0, 1 and 2.

The implementation uses the Knuth‑Morris‑Pratt (KMP) algorithm which runs in
``O(len(haystack) + len(needle))`` time and ``O(len(needle))`` extra space –
fast even for very large inputs.

The function returns ``0`` for an empty ``needle`` (consistent with the
behaviour of most string‑search utilities).
"""

from __future__ import annotations

__all__ = ["count_overlapping"]


def _build_kmp_table(pattern: str) -> list[int]:
    """Build the partial‑match (failure) table for KMP.

    The table stores, for each position ``i`` in ``pattern``, the length of the
    longest proper prefix of ``pattern[:i]`` which is also a suffix.  This allows
    the search to skip characters when a mismatch occurs.
    """
    m = len(pattern)
    table = [0] * (m + 1)
    # ``pos`` is the current position we are computing, ``cnd`` is the index of
    # the next character of the candidate substring.
    pos, cnd = 1, 0
    while pos < m:
        if pattern[pos] == pattern[cnd]:
            cnd += 1
            pos += 1
            table[pos] = cnd
        elif cnd > 0:
            cnd = table[cnd]
        else:
            pos += 1
            table[pos] = 0
    return table


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of *overlapping* occurrences of ``needle`` in ``haystack``.

    Parameters
    ----------
    haystack: str
        The string to be searched.
    needle: str
        The substring to look for.  An empty ``needle`` yields ``0``.

    Returns
    -------
    int
        Count of overlapping matches.
    """
    if not needle:
        return 0
    n, m = len(haystack), len(needle)
    if m > n:
        return 0

    # Pre‑process the pattern.
    table = _build_kmp_table(needle)
    i = j = 0  # i → index in haystack, j → index in needle
    count = 0
    while i < n:
        if haystack[i] == needle[j]:
            i += 1
            j += 1
            if j == m:
                count += 1
                # For overlapping we continue searching from the longest
                # proper prefix which is also a suffix.
                j = table[j]
        else:
            if j > 0:
                j = table[j]
            else:
                i += 1
    return count
