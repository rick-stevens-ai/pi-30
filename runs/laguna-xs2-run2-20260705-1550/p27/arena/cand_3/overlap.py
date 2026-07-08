"""Count overlapping occurrences of a substring in a string."""


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return the number of overlapping occurrences of needle in haystack.
    
    Examples:
        >>> count_overlapping('aaaa', 'aa')
        3
        >>> count_overlapping('abcabc', 'abc')
        2
        >>> count_overlapping('abc', '')
        0
    """
    if not needle:
        return 0
    
    n = len(needle)
    m = len(haystack)
    
    if n > m:
        return 0
    
    # Use find() in a loop, advancing by 1 each time to allow overlaps
    count = 0
    start = 0
    while start <= m - n:
        pos = haystack.find(needle, start)
        if pos == -1:
            break
        count += 1
        start = pos + 1  # Move just 1 character to allow overlapping matches
    
    return count


if __name__ == '__main__':
    import doctest
    doctest.testmod()