"""Count overlapping occurrences of a substring in a string.

Uses KMP algorithm for O(n+m) time complexity.
"""

__all__ = ['count_overlapping']


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count overlapping occurrences of needle in haystack.

    Unlike str.count(), this counts overlapping matches.
    E.g., count_overlapping('aaaa', 'aa') == 3

    Args:
        haystack: The string to search in.
        needle: The substring to search for.

    Returns:
        Number of overlapping occurrences, or 0 if needle is empty.
    """
    if not needle:
        return 0

    n, m = len(haystack), len(needle)

    # Build KMP failure function (longest proper prefix which is also suffix)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if needle[i] == needle[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    # Search using KMP, allowing overlaps
    count = 0
    i = 0  # index for haystack
    j = 0  # index for needle

    while i < n:
        if needle[j] == haystack[i]:
            i += 1
            j += 1

        if j == m:
            count += 1
            j = lps[j - 1]  # For overlapping matches, use lps to continue
        elif i < n and needle[j] != haystack[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return count