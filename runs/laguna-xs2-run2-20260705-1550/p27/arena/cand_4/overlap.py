"""Count overlapping string occurrences using KMP algorithm."""


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count overlapping occurrences of needle in haystack.

    Uses Knuth-Morris-Pratt algorithm for O(n+m) time complexity.

    Args:
        haystack: The string to search in.
        needle: The pattern to search for.

    Returns:
        Number of overlapping occurrences. Returns 0 for empty needle.

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

    m = len(needle)
    n = len(haystack)

    # Build KMP failure function (partial match table / LPS array)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if needle[i] == needle[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    # Search using KMP
    count = 0
    i = 0  # Index for haystack
    j = 0  # Index for needle

    while i < n:
        if needle[j] == haystack[i]:
            i += 1
            j += 1

        if j == m:
            count += 1
            j = lps[j - 1]
        elif i < n and needle[j] != haystack[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return count