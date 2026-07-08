"""Overlapping string matching - count overlapping occurrences."""


def count_overlapping(haystack: str, needle: str) -> int:
    """Return number of overlapping occurrences of needle in haystack.
    
    Examples:
        count_overlapping('aaaa', 'aa') == 3
        count_overlapping('abcabc', 'abc') == 2
        count_overlapping('abc', '') == 0
    """
    if not needle:
        return 0
    
    n = len(needle)
    h = len(haystack)
    
    if n > h:
        return 0
    
    # Single char is very common - use stdlib count for speed
    if n == 1:
        return haystack.count(needle)
    
    # For longer needles, count all positions with slice comparison
    count = 0
    limit = h - n + 1
    for i in range(limit):
        if haystack[i:i + n] == needle:
            count += 1
    return count