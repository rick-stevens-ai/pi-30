# overlap.py
"""Utility to count overlapping occurrences of a substring.

Provides ``count_overlapping`` which returns the number of (potentially overlapping)
occurrences of *needle* inside *haystack*.

Examples
--------
>>> count_overlapping('aaaa', 'aa')
3
>>> count_overlapping('abababa', 'aba')
3
>>> count_overlapping('test', '')
0

The implementation uses ``str.find`` in a loop, advancing the start index by one
after each match to allow overlapping matches. This runs in O(n) time on average
for typical inputs and requires only the Python standard library.
"""

from __future__ import annotations

__all__ = ["count_overlapping"]


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of (overlapping) occurrences of *needle* in *haystack*.

    Parameters
    ----------
    haystack: str
        The string to search within.
    needle: str
        The substring to look for. An empty ``needle`` yields ``0`` per the
        specification.

    Returns
    -------
    int
        Count of overlapping occurrences.
    """
    if not needle:
        # By definition, an empty needle does not match anything.
        return 0

    count = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        # Move just one position forward to allow overlapping matches.
        start = idx + 1
    return count


if __name__ == "__main__":
    # Simple sanity check when run as a script.
    import sys
    if len(sys.argv) != 3:
        print("Usage: python overlap.py <haystack> <needle>")
        sys.exit(1)
    print(count_overlapping(sys.argv[1], sys.argv[2]))
