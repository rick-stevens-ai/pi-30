def count_overlapping(haystack, needle):
    """
    Return the number of overlapping occurrences of `needle` in `haystack`.

    An empty needle yields 0. The algorithm runs in O(len(haystack)) by using
    `str.find` which is implemented in C, making it fast for long strings.
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
        # Move start one character after the current match to allow overlapping.
        start = idx + 1
    return count


if __name__ == "__main__":
    # Simple sanity checks (optional)
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("", "a") == 0
    assert count_overlapping("abc", "") == 0
    assert count_overlapping("abcdef", "xyz") == 0
    print("overlap.py loaded successfully")