import re

def count_overlapping(haystack: str, needle: str) -> int:
    """Count OVERLAPPING occurrences of needle in haystack.
    
    Args:
        haystack: String to search in
        needle: Substring to count (empty -> 0)
    
    Returns:
        Number of overlapping occurrences
        >>> count_overlapping('aaaa', 'aa')
        3
    >>> count_overlapping('ababab', 'aba')
        2
    >>> count_overlapping('hello', '')
        0
    >>> count_overlapping('', 'a')
        0
    """
    if not needle:
        return 0
    # Use regex lookahead to find overlapping matches.
    # re.finditer with (?=...) finds zero-width matches at each position.
    # This is implemented in C and very fast for long strings.
    pattern = '(?=' + re.escape(needle) + ')'
    return sum(1 for _ in re.finditer(pattern, haystack))


if __name__ == '__main__':
    import doctest
    doctest.testmod()