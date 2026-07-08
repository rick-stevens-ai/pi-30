def count_overlapping(text: str, pattern: str) -> int:
    """
    Return the number of (possibly overlapping) occurrences of pattern in text.
    Overlapping occurrences are counted.
    """
    if not pattern:
        return 0
    count = 0
    start = 0
    while True:
        idx = text.find(pattern, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1  # allow overlapping
    return count


if __name__ == "__main__":
    # Simple tests
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("abcabc", "abc") == 2
    assert count_overlapping("aaaa", "a") == 4
    assert count_overlapping("abc", "d") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("", "") == 0
    print("All tests passed")
