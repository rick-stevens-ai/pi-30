"""Count overlapping occurrences of a needle in a haystack."""
import re


def count_overlapping(haystack: str, needle: str) -> int:
    """Return number of overlapping occurrences of needle in haystack.
    
    Counts 'aa' in 'aaaa' == 3 (unlike str.count which returns 2).
    Returns 0 for empty needle.
    
    Args:
        haystack: The string to search in.
        needle: The pattern to search for.
        
    Returns:
        Number of overlapping occurrences.
    """
    if not needle:
        return 0
    
    # Use positive lookahead to find all overlapping matches
    # (?=pattern) matches at every position where pattern could start
    pattern = r'(?=' + re.escape(needle) + ')'
    return len(re.findall(pattern, haystack))