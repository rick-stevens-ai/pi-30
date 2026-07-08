"""Count overlapping occurrences of a substring in a string."""


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count overlapping occurrences of needle in haystack.
    
    Unlike str.count(), this counts overlapping matches.
    E.g., count_overlapping('aaaa', 'aa') == 3
    
    Args:
        haystack: The string to search in
        needle: The substring to find
        
    Returns:
        Number of overlapping occurrences, or 0 if needle is empty
    """
    if not needle:
        return 0
    
    n = len(needle)
    m = len(haystack)
    
    if n > m:
        return 0
    
    # Use KMP (Knuth-Morris-Pratt) for O(n+m) time complexity
    # Build the prefix function (failure function)
    prefix = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and needle[i] != needle[j]:
            j = prefix[j - 1]
        if needle[i] == needle[j]:
            j += 1
            prefix[i] = j
    
    # Search using the prefix function
    count = 0
    j = 0
    for i in range(m):
        while j > 0 and haystack[i] != needle[j]:
            j = prefix[j - 1]
        if haystack[i] == needle[j]:
            j += 1
        if j == n:
            count += 1
            j = prefix[j - 1]  # Continue searching for more matches
    
    return count