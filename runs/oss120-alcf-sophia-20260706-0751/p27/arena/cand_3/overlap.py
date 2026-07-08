# overlap.py
"""Utility to count overlapping occurrences of a substring.

The standard :py:meth:`str.count` does **not** count overlapping matches:

>>> 'aaaa'.count('aa')
2

For many bio‑informatics and text‑processing tasks we need the overlapping
count, i.e. ``'aa'`` occurs three times in ``'aaaa'`` (positions 0‑1, 1‑2 and
2‑3).  This module provides :func:`count_overlapping` which returns that
integer count.

The implementation uses the Knuth‑Morris‑Pratt (KMP) algorithm to achieve
`O(n + m)` time where *n* is the length of the haystack and *m* the length of
the needle.  Only the Python standard library is required.

Edge cases:

* An empty ``needle`` yields ``0`` (consistent with the behaviour of many
  regular‑expression engines and with the expectation expressed in the task).
* If ``needle`` is longer than ``haystack`` the result is ``0``.
"""

from __future__ import annotations

from typing import List

__all__: List[str] = ["count_overlapping"]


def _build_kmp_table(pattern: str) -> List[int]:
    """Construct the partial‑match table (also known as "failure function").

    For each position ``i`` in the pattern, ``table[i]`` is the length of the
    longest proper prefix of ``pattern[:i+1]`` that is also a suffix of that
    substring.  The table is used to skip comparisons when a mismatch occurs.
    """
    m = len(pattern)
    table = [0] * m
    j = 0  # length of previous longest prefix suffix

    # The first character has no proper prefix/suffix.
    for i in range(1, m):
        # Fall back in the pattern until we find a match or reach the start.
        while j > 0 and pattern[i] != pattern[j]:
            j = table[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            table[i] = j
        # else table[i] stays 0
    return table


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of **overlapping** occurrences of ``needle`` in ``haystack``.

    Parameters
    ----------
    haystack: str
        The string to search within.
    needle: str
        The substring to search for.  An empty needle returns ``0``.

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

    # Build KMP failure table for the needle.
    table = _build_kmp_table(needle)

    count = 0
    i = 0  # index in haystack
    j = 0  # index in needle
    while i < n:
        if haystack[i] == needle[j]:
            i += 1
            j += 1
            if j == m:
                # Full match found ending at position i-1.
                count += 1
                # For overlapping matches we continue searching using the
                # longest proper prefix which is also a suffix.
                j = table[j - 1]  # may be 0, allowing the next search to start at i-m+1+1
        else:
            if j != 0:
                j = table[j - 1]
            else:
                i += 1
    return count

# Simple sanity test when the module is executed directly.
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python overlap.py <haystack> <needle>")
        sys.exit(1)
    print(count_overlapping(sys.argv[1], sys.argv[2]))
