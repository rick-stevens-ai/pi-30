def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count the number of overlapping occurrences of needle in haystack.
    
    Args:
        haystack: The string to search within
        needle: The substring to search for
    
    Returns:
        The count of overlapping occurrences
    
    Examples:
        count_overlapping('aaaa', 'aa') -> 3
        count_overlapping('aaa', 'aa') -> 2
        count_overlapping('', 'aa') -> 0
        count_overlapping('abc', '') -> 0
    """
    if not needle:
        return 0
    
    count = 0
    n = len(needle)
    for i in range(len(haystack) - n + 1):
        if haystack[i:i+n] == needle:
            count += 1
    
    return count
