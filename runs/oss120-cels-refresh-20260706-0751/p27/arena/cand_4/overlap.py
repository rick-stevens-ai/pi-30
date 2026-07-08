# overlap.py
"""Utility for counting overlapping occurrences of a substring.

The function :func:`count_overlapping` returns the number of times *needle*
appears in *haystack*, allowing occurrences to overlap.  For example::

    >>> count_overlapping('aaaa', 'aa')
    3

An empty *needle* is defined to have zero occurrences.

The implementation uses the Knuth‑Morris‑Pratt (KMP) algorithm, which runs
in O(n + m) time where *n* is the length of *haystack* and *m* is the length of
*needle*.  This makes it fast even for very long strings.
"""

from __future__ import annotations


def _build_prefix_table(pattern: str) -> list[int]:
    """Build the KMP prefix (also called "failure") table.

    ``prefix[i]`` is the length of the longest proper prefix of ``pattern[:i+1]``
    that is also a suffix of that substring.
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
    """Return the number of (potentially overlapping) occurrences of ``needle``
    in ``haystack``.

    The function runs in linear time with respect to the lengths of the two
    strings.  If ``needle`` is empty, ``0`` is returned, matching the behaviour
    required by the problem statement.
    """
    if not needle:
        return 0

    n, m = len(haystack), len(needle)
    if m > n:
        return 0

    # Pre‑process the pattern.
    prefix = _build_prefix_table(needle)

    count = 0
    q = 0  # number of characters matched
    for i in range(n):
        while q > 0 and needle[q] != haystack[i]:
            q = prefix[q - 1]
        if needle[q] == haystack[i]:
            q += 1
        if q == m:
            count += 1
            # For overlapping matches we continue searching from the longest
            # proper prefix which is also a suffix.
            q = prefix[q - 1]
    return count


if __name__ == "__main__":
    # Simple sanity checks when run as a script.
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("ababab", "aba") == 2
    assert count_overlapping("abc", "d") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("abc", "") == 0
    print("All quick tests passed.")
