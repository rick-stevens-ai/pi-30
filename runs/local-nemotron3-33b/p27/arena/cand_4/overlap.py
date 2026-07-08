def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return the number of overlapping occurrences of `needle` in `haystack`.

    Examples:
        count_overlapping('aaaa', 'aa')  # -> 3
        count_overlapping('abcabc', 'ab')  # -> 2
        count_overlapping('abc', '')  # -> 0

    The implementation uses a sliding window with str.find to stay within the
    Python standard library and remains efficient for long strings.
    """
    if not needle:
        return 0

    count = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        # Move only one character forward to allow overlapping matches.
        start = idx + 1
    return count