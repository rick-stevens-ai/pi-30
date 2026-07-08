"""Count overlapping string occurrences using regex lookahead."""

import re


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count overlapping occurrences of needle in haystack.
    
    Uses a lookahead assertion trick: (?=needle) finds all positions
    where needle starts, including overlapping ones.
    
    Args:
        haystack: The string to search in.
        needle: The substring to find.
    
    Returns:
        Number of overlapping occurrences. Returns 0 for empty needle.
    
    Examples:
        >>> count_overlapping('aaaa', 'aa')
        3
        >>> count_overlapping('abcabc', 'abc')
        2
        >>> count_overlapping('hello', '')
        0
        >>> count_overlapping('', 'a')
        0
    """
    if not needle:
        return 0
    
    # Escape special regex chars in needle, then wrap in lookahead
    pattern = f'(?={re.escape(needle)})'
    return len(re.findall(pattern, haystack))