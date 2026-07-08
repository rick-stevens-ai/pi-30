def count_Overlapping(haystack, needle):
    """Return the number of overlapping occurrences of needle in haystack."""
    if not needle:
        return 0
    count = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1  # Move one character forward to allow overlaps.
    return count


if __name__ == "__main__":
    # Simple sanity checks
    assert count_Overlapping("aaaa", "aa") == 3
    assert count_Overlapping("abcabcabc", "abc") == 3
    assert count_Overlapping("ababa", "aba") == 2
    assert count_Overlapping("", "a") == 0
    assert count_Overlapping("anything", "") == 0
    print("All tests passed.")