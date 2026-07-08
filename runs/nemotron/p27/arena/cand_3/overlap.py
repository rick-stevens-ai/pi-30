"""Overlapping substring count using KMP algorithm for O(n+m) guaranteed performance."""

def _build_lps(pattern: str) -> list[int]:
    """Build longest proper prefix which is also suffix (LPS) array for KMP."""
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of previous longest prefix suffix
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count OVERLAPPING occurrences of needle in haystack.
    
    Args:
        haystack: String to search in
        needle: Substring to search for
        
    Returns:
        Number of overlapping occurrences (empty needle -> 0)
        
    Examples:
        >>> count_overlapping('aaaa', 'aa')
        3
        >>> count_overlapping('abababa', 'aba')
        3
        >>> count_overlapping('hello', '')
        0
    """
    if not needle:
        return 0
    
    n, m = len(haystack), len(needle)
    if m > n:
        return 0
    
    lps = _build_lps(needle)
    count = 0
    i = j = 0  # i for haystack, j for needle
    
    while i < n:
        if haystack[i] == needle[j]:
            i += 1
            j += 1
            if j == m:
                count += 1
                # For overlapping: use LPS to continue search
                j = lps[j - 1]
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
    
    return count


if __name__ == "__main__":
    # Basic tests
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("abababa", "aba") == 3
    assert count_overlapping("hello", "") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("abc", "abcd") == 0
    assert count_overlapping("abcabc", "abc") == 2
    assert count_overlapping("aaaaa", "aaa") == 3
    assert count_overlapping("mississippi", "issi") == 2
    assert count_overlapping("aaaaaaaaaa", "aa") == 9
    print("All tests passed!")