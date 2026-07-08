def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of needle in haystack.
    Returns 0 if needle is empty.
    """
    if not needle:
        return 0
    
    count = 0
    pos = 0
    while True:
        pos = haystack.find(needle, pos)
        if pos == -1:
            break
        count += 1
        pos += 1
    return count

if __name__ == "__main__":
    # Test cases
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("banana", "ana") == 2
    assert count_overlapping("abcde", "f") == 0
    assert count_overlapping("aaaaa", "aaa") == 3
    assert count_overlapping("mississippi", "issi") == 2
    assert count_overlapping("aaaaa", "") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("", "") == 0
    print("All tests passed!")
