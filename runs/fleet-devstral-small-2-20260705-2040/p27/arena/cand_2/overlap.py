def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count the number of overlapping occurrences of needle in haystack.
    
    Examples:
        count_overlapping('aaaa', 'aa') -> 3
        count_overlapping('', 'x') -> 0
        count_overlapping('x', '') -> 0
    """
    if not needle:
        return 0
    n = len(needle)
    count = 0
    for i in range(len(haystack) - n + 1):
        if haystack[i:i+n] == needle:
            count += 1
    return count
