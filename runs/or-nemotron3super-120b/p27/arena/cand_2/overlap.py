def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return the number of overlapping occurrences of needle in haystack.
    Empty needle returns 0.
    """
    if not needle:
        return 0
    count = 0
    start = 0
    while True:
        pos = haystack.find(needle, start)
        if pos == -1:
            break
        count += 1
        start = pos + 1  # move one character ahead for overlapping
    return count

# Simple self-test
if __name__ == "__main__":
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("", "a") == 0
    assert count_overlapping("abc", "") == 0
    assert count_overlapping("abcabc", "abc") == 2
    assert count_overlapping("aaaaa", "aa") == 4
    assert count_overlapping("ababababa", "aba") == 4  # positions 0,2,4,6
    print("All tests passed")