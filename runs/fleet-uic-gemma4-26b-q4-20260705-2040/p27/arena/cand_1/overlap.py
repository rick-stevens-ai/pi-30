def count_overlapping(haystack: str, needle: str) -> int:
    """
    Returns the number of overlapping occurrences of `needle` in `haystack`.
    
    Example:
        count_overlapping("aaaa", "aa") == 3
        count_overlapping("abcde", "") == 0
    """
    if not needle:
        return 0
    
    count = 0
    start = 0
    while True:
        start = haystack.find(needle, start)
        if start == -1:
            break
        count += 1
        start += 1
    return count

if __name__ == "__main__":
    # Quick manual tests
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("aaaaa", "aa") == 4
    assert count_overlapping("ababa", "aba") == 2
    assert count_overlapping("banana", "ana") == 2
    assert count_overlapping("abcde", "f") == 0
    assert count_overlapping("abcde", "") == 0
    print("All manual tests passed!")
