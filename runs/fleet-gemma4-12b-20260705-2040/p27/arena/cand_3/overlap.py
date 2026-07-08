def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of a needle string within a haystack string.
    Returns 0 if the needle is empty.

    Example:
        count_overlapping('aaaa', 'aa') == 3
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
        start = idx + 1
    return count

if __name__ == "__main__":
    # Basic tests
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("banana", "ana") == 2
    assert count_overlapping("aaaaa", "aaa") == 3
    assert count_overlapping("abc", "d") == 0
    assert count_overlapping("abc", "") == 0
    assert count_overlapping("", "a") == 0

    # Long string performance test (roughly)
    large_haystack = "a" * 1000000
    needle = "aa"
    # Expected: 999,999 overlaps
    # 'aaaa' -> 3. Length N, needle length 2 -> N-1 overlaps if all match.
    assert count_overlapping(large_haystack, needle) == 999999
    print("All tests passed!")
