"""
overlap.py – expose count_overlapping(haystack, needle) → int

Count the number of (possibly overlapping) occurrences of `needle`
within `haystack`.  Overlapping matches are counted by moving the
search start position forward only one character after each match,
unlike str.count which advances by the length of the pattern.

The implementation uses only the Python standard library and is
optimised for long strings:
* Empty needle yields 0 (matching the behaviour of most expectation‑
  based APIs).
* Uses `str.find` with a incremental start offset, which runs in C
  inside CPython and therefore remains fast even on very large inputs.

Example
-------
>>> count_overlapping('aaaa', 'aa')
3
>>> count_overlapping('banana', 'na')
2
>>> count_overlapping('abcdef', '')
0
"""

from __future__ import annotations

def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return the number of overlapping occurrences of ``needle`` in ``haystack``.

    Parameters
    ----------
    haystack : str
        The string to search inside.
    needle : str
        The substring pattern to look for.  If empty, returns 0.

    Returns
    -------
    int
        Number of (possibly overlapping) matches.

    Notes
    -----
    * ``needle == ''`` → 0 (the function deliberately treats an empty pattern as
      having no matches).
    * The search is case‑sensitive and works on any Unicode strings.
    * Implementation relies exclusively on the standard library; it runs in
      C under the hood via :meth:`str.find` and therefore scales well to large
      inputs.

    Examples
    --------
    >>> count_overlapping('aaaa', 'aa')
    3
    >>> count_overlapping('banana', 'na')
    2
    >>> count_overlapping('hello', 'world')
    0
    """
    # Empty needle has no meaningful matches.
    if not needle:
        return 0

    count = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        # Move only one character forward to allow overlapping matches.
        start = idx + 1
    return count

# Expose a convenient alias for ``pip``/import use.
__all__ = ["count_overlapping"]