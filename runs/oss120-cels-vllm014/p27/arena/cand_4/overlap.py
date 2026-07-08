# overlap.py
"""Utility to count overlapping occurrences of a substring.

The standard :py:meth:`str.count` does **not** count overlapping matches::

    >>> 'aaaa'.count('aa')
    2

For many text‑processing tasks we need the overlapping count, e.g. ``'aaaa'``
contains ``'aa'`` three times (positions 0‑1, 1‑2 and 2‑3).

The :func:`count_overlapping` function implements this efficiently using the
Knuth‑Morris‑Pratt (KMP) algorithm, which runs in ``O(n + m)`` time where ``n``
is the length of the haystack and ``m`` is the length of the needle.  It uses
only the Python standard library.

Edge cases:

* An empty ``needle`` returns ``0`` – there is no sensible definition of
  overlapping matches for an empty pattern.
* The function works with any Unicode strings.
"""

from __future__ import annotations

__all__ = ["count_overlapping"]


def _prefix_function(pattern: str) -> list[int]:
    """Return the KMP prefix (failure) function for *pattern*.

    ``prefix[i]`` is the length of the longest proper prefix of ``pattern[:i+1]``
    that is also a suffix of this substring.
    """
    m = len(pattern)
    prefix = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = prefix[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        prefix[i] = k
    return prefix


def count_overlapping(haystack: str, needle: str) -> int:
    """Count **overlapping** occurrences of *needle* in *haystack*.

    Parameters
    ----------
    haystack: str
        The string to search within.
    needle: str
        The substring pattern to look for.

    Returns
    -------
    int
        Number of (possibly overlapping) matches.

    Notes
    -----
    The implementation uses the Knuth‑Morris‑Pratt algorithm which
    guarantees linear time complexity with respect to the total input size.
    """
    if not needle:
        # By definition we treat an empty pattern as having no matches.
        return 0

    prefix = _prefix_function(needle)
    count = 0
    j = 0  # current length of matched prefix of needle
    n = len(haystack)
    m = len(needle)

    for i in range(n):
        # Advance the match length `j` while characters differ.
        while j > 0 and haystack[i] != needle[j]:
            j = prefix[j - 1]
        if haystack[i] == needle[j]:
            j += 1
            if j == m:
                count += 1
                # Prepare `j` for the next possible (overlapping) match.
                j = prefix[j - 1]
        # else: j stays 0
    return count


# Simple sanity‑check when executed as a script.
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python overlap.py <haystack> <needle>")
        sys.exit(1)
    h, n = sys.argv[1], sys.argv[2]
    print(count_overlapping(h, n))
