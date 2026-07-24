def count_overlapping(haystack, needle):
    """Return number of OVERLAPPING occurrences of needle in haystack."""
    if not needle:
        return 0
    count = 0
    idx = haystack.find(needle)
    while idx != -1:
        count += 1
        idx = haystack.find(needle, idx + 1)
    return count

if __name__ == "__main__":
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("aaaa", "") == 0
    assert count_overlapping("hello", "ll") == 1
    assert count_overlapping("abababa", "aba") == 3
    print("OK")
