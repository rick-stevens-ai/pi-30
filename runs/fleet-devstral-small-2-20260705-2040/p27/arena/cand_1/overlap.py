"""
Count overlapping occurrences of needle in haystack.

For example:
    count_overlapping('aaaa', 'aa') -> 3
    count_overlapping('aaaa', 'a') -> 4
    count_overlapping('abcabc', 'abc') -> 2
    count_overlapping('abcabc', 'ab') -> 3
    count_overlapping('abcabc', 'b') -> 2
    count_overlapping('abcabc', 'c') -> 2
    count_overlapping('abcabc', 'd') -> 0
    count_overlapping('abcabc', '') -> 0
"""

from typing import Optional


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count overlapping occurrences of needle in haystack.

    Args:
        haystack: The string to search within.
        needle: The substring to search for.

    Returns:
        The number of overlapping occurrences of needle in haystack.
        Returns 0 if needle is empty.
    """
    if not needle:
        return 0

    n = len(needle)
    count = 0
    i = 0
    while i <= len(haystack) - n:
        if haystack[i:i+n] == needle:
            count += 1
            i += 1  # Move by 1 to allow overlaps
        else:
            i += 1
    return count
