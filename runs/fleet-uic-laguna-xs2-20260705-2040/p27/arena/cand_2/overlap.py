"""Count overlapping string occurrences."""


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count overlapping occurrences of needle in haystack.

    Args:
        haystack: The string to search in.
        needle: The string to search for.

    Returns:
        Number of overlapping occurrences. Returns 0 for empty needle.

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

    count = 0
    start = 0
    needle_len = len(needle)

    while start <= len(haystack) - needle_len:
        pos = haystack.find(needle, start)
        if pos == -1:
            break
        count += 1
        start = pos + 1  # Advance by 1 for overlapping matches

    return count


if __name__ == '__main__':
    # Quick tests
    assert count_overlapping('aaaa', 'aa') == 3, "Overlapping 'aa' in 'aaaa'"
    assert count_overlapping('abababa', 'aba') == 3, "Overlapping 'aba'"
    assert count_overlapping('hello world', 'l') == 3, "Overlapping 'l'"
    assert count_overlapping('hello', '') == 0, "Empty needle"
    assert count_overlapping('', 'x') == 0, "Needle not in empty haystack"
    assert count_overlapping('abc', '') == 0, "Empty needle in non-empty haystack"
    assert count_overlapping('abcabc', 'abc') == 2, "Non-overlapping default"
    print("All tests passed!")