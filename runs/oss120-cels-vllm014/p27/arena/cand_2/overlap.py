"""Utility for counting overlapping occurrences of a substring.

Provides :func:`count_overlapping` which returns the number of (potentially
overlapping) matches of *needle* in *haystack*.

Example
-------
>>> count_overlapping('aaaa', 'aa')
3
>>> count_overlapping('abababa', 'aba')
3

The implementation uses a Knuth‑Morris‑Pratt (KMP) automaton so the runtime is
O(len(haystack) + len(needle)) and works with arbitrarily long strings while
relying only on the Python standard library.
"""

from __future__ import annotations

__all__ = ["count_overlapping"]


def _build_kmp_table(pattern: str) -> list[int]:
    """Return the KMP "failure" table for *pattern*.

    ``table[i]`` is the length of the longest proper prefix of ``pattern[:i]``
    that is also a suffix of ``pattern[:i]``.  The table start with ``0`` for the
    first character.
    """
    length = len(pattern)
    table = [0] * length
    # ``pos`` is the current position we are computing the table for, ``cnd``
    # stores the length of the current candidate prefix.
    cnd = 0
    for pos in range(1, length):
        while cnd > 0 and pattern[pos] != pattern[cnd]:
            cnd = table[cnd - 1]
        if pattern[pos] == pattern[cnd]:
            cnd += 1
            table[pos] = cnd
        else:
            table[pos] = 0
    return table


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of (possibly overlapping) occurrences of *needle*.

    Parameters
    ----------
    haystack: str
        The string to search within.
    needle: str
        The substring to look for.  An empty needle yields ``0`` as there is no
        sensible definition of overlapping matches.

    Returns
    -------
    int
        Count of overlapping matches.
    """
    if not needle:
        return 0
    if len(needle) == 1:
        # Fast path for single‑character needle – ``str.count`` already counts
        # each character, which is the same as overlapping occurrences.
        return haystack.count(needle)

    # Build the KMP failure table for the pattern.
    table = _build_kmp_table(needle)
    i = 0  # index in haystack
    j = 0  # index in needle (length of current match)
    count = 0
    h_len = len(haystack)
    n_len = len(needle)

    while i < h_len:
        if haystack[i] == needle[j]:
            i += 1
            j += 1
            if j == n_len:
                # Full match found – increment count and continue searching
                # using the failure link to allow overlapping matches.
                count += 1
                j = table[j - 1]  # jump to the longest proper prefix
        else:
            if j != 0:
                j = table[j - 1]
            else:
                i += 1
    return count
