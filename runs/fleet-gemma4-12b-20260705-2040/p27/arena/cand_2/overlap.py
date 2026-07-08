def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of 'needle' in 'haystack'.
    Returns 0 if 'needle' is empty.

    Example:
        count_overlapping('aaaa', 'aa') -> 3
        count_overlapping('banana', 'ana') -> 2
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
    # Test cases
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("banana", "ana") == 2
    assert count_overlapping("aaaaa", "aaa") == 3
    assert count_overlapping("abc", "") == 0
    assert count_overlapping("mississippi", "issi") == 2
    assert count_overlapping("aaaaaaaaaa", "aaa") == 8
    print("Tests passed!")
