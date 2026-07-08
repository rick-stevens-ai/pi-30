"""
Count overlapping occurrences of needle in haystack.

Examples:
    overlap.count_overlapping('aaaa', 'aa') == 3
    overlap.count_overlapping('ababab', 'aba') == 2
    overlap.count_overlapping('', '') == 0
    overlap.count_overlapping('aaa', '') == 0
"""

def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count overlapping occurrences of needle in haystack.
    
    Args:
        haystack: The string to search in
        needle: The substring to find (empty always returns 0)
    
    Returns:
        Number of overlapping occurrences
    """
    if not needle:
        return 0
    
    count = 0
    n = len(needle)
    h_len = len(haystack)
    
    # If haystack is shorter than needle, no matches possible
    if h_len < n:
        return 0
    
    # Precompute the longest prefix which is also suffix (KMP failure function)
    failure = [0] * n
    j = 0
    for i in range(1, n):
        j = failure[i - 1]
        while j > 0 and needle[i] != needle[j]:
            j = failure[j - 1]
        if needle[i] == needle[j]:
            j += 1
            failure[i] = j
        else:
            failure[i] = 0
    
    # Search with overlapping matches
    for i in range(h_len - n + 1):
        if haystack[i:i+n] == needle:
            count += 1
    
    return count if haystack else 0
