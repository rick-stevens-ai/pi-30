"""Count overlapping string occurrences.

This module provides an efficient function to count overlapping occurrences
of a substring within a string, where str.count() does not overlap.
"""


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of overlapping occurrences of needle in haystack.

    Unlike str.count(), this counts overlapping matches:
        count_overlapping('aaaa', 'aa') == 3
        'aaaa'.count('aa') == 2  # does not overlap

    Args:
        haystack: The string to search in.
        needle: The substring to search for.

    Returns:
        Number of overlapping occurrences. Returns 0 for empty needle.

    Examples:
        >>> count_overlapping('aaaa', 'aa')
        3
        >>> count_overlapping('abababa', 'aba')
        3
        >>> count_overlapping('hello', '')
        0
        >>> count_overlapping('', 'x')
        0
    """
    if not needle:
        return 0

    count = 0
    start = 0
    while True:
        pos = haystack.find(needle, start)
        if pos == -1:
            break
        count += 1
        start = pos + 1  # Advance just one char to catch overlaps
    return count