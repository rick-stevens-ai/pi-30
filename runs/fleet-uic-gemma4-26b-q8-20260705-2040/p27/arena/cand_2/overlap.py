import time

def count_overlapping(haystack, needle):
    """
    Counts the number of overlapping occurrences of 'needle' in 'haystack'.
    Returns 0 if 'needle' is empty.
    """
    if not needle:
        return 0
    
    count = 0
    idx = haystack.find(needle)
    while idx != -1:
        count += 1
        idx = haystack.find(needle, idx + 1)
    return count

def test():
    # Basic tests
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("banana", "ana") == 2
    assert count_overlapping("aaaaa", "aaa") == 3
    assert count_overlapping("abcde", "f") == 0
    assert count_overlapping("aaaaa", "") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("", "") == 0
    print("Basic tests passed!")

    # Performance test (large haystack)
    haystack = "a" * 1_000_000
    needle = "aa"
    start_time = time.time()
    result = count_overlapping(haystack, needle)
    end_time = time.time()
    print(f"Result: {result}, Time: {end_time - start_time:.4f}s")
    assert result == 999_999

    # Performance test (needle not found)
    haystack = "a" * 1_000_000
    needle = "b"
    start_time = time.time()
    result = count_overlapping(haystack, needle)
    end_time = time.time()
    print(f"Non-found Result: {result}, Time: {end_time - start_time:.4f}s")
    assert result == 0

if __name__ == "__main__":
    test()
