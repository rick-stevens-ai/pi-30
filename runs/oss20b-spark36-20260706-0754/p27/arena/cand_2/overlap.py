"""
Count overlapping substrings.

This module exposes a single function ``count_overlapping`` that counts the number of
occurrences of *needle* in *haystack*, including overlapping matches.  The implementation
uses the Knuth‑Morris‑Pratt (KMP) algorithm, giving linear time behaviour with respect
to the length of `haystack` and `needle`, and is fully based on Python standard library.

Examples
--------
>>> count_overlapping('aaaa', 'aa')
3
>>> count_overlapping('abababa', 'aba')
2
>>> count_overlapping('abc', '')
0
"""

from __future__ import annotations

def _build_lps(pattern: str) -> list[int]:
    """Return the longest‑prefix‐suffix (LPS) array for *pattern*.

    The LPS array is used by KMP to determine how far we can skip when a mismatch
    occurs.  For example, ``pattern = 'ABCDABD'`` yields ``[0,0,0,0,1,2,0]``.
    """
    n = len(pattern)
    lps = [0] * n
    length = 0  # length of the previous longest prefix suffix
    i = 1
    while i < n:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of overlapping occurrences of *needle* in *haystack*.

    The function handles empty needles explicitly because an empty pattern would
    otherwise match every position in ``haystack`` and lead to infinite matches.

    Parameters
    ----------
    haystack: str
        Text where to search.
    needle: str
        Sub‑string to look for.

    Returns
    -------
    int
        Count of overlapping matches.  ``0`` is returned if *needle* is empty.
    """
    if not needle:
        return 0
    n = len(needle)
    m = len(haystack)
    lps: list[int] = _build_lps(needle)
    i = j = count = 0  # i over haystack, j over needle
    while i < m:
        if haystack[i] == needle[j]:
            i += 1
            j += 1
            if j == n:
                count += 1
                # Move to the longest prefix which is also a suffix
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return count

__all__ = ["count_overlapping"]
