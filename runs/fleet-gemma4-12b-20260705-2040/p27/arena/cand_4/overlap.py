def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of 'needle' in 'haystack'.
    For example, count_overlapping('aaaa', 'aa') returns 3.
    An empty needle always returns 0.
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
        # Move forward by only 1 to allow for overlapping matches
        start = pos + 1
        
    return count

if __name__ == "__main__":
    # Test cases
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("banana", "ana") == 2
    assert count_overlapping("aaaaa", "aaa") == 3
    assert count_overlapping("abc", "d") == 0
    assert count_overlapping("abc", "") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("aaaaa", "aaaa") == 2
    print("All tests passed!")
