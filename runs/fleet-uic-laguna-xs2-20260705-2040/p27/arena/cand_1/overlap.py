import re


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count overlapping occurrences of needle in haystack.
    
    Examples:
        count_overlapping('aaaa', 'aa') == 3
        count_overlapping('abcabc', 'abc') == 2
        count_overlapping('aaaa', '') == 0
    
    Args:
        haystack: The string to search in
        needle: The pattern to search for
    
    Returns:
        Number of overlapping occurrences (0 for empty needle)
    """
    if not needle:
        return 0
    
    # Use lookahead assertion to find all overlapping matches
    # (?=...) is a positive lookahead that doesn't consume characters
    pattern = f'(?=({re.escape(needle)}))'
    return len(re.findall(pattern, haystack))