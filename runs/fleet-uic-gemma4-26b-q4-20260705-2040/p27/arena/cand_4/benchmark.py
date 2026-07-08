import time
import re

def count_overlapping_find(haystack, needle):
    if not needle:
        return 0
    count = 0
    start = 0
    n = len(needle)
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count

def count_overlapping_regex(haystack, needle):
    if not needle:
        return 0
    # We need to escape the needle in case it contains regex special characters
    pattern = f'(?={re.escape(needle)})'
    return len(re.findall(pattern, haystack))

def test():
    assert count_overlapping_find('aaaa', 'aa') == 3
    assert count_overlapping_find('banana', 'ana') == 2
    assert count_overlapping_find('aaaaa', 'aa') == 4
    assert count_overlapping_find('abcde', 'f') == 0
    assert count_overlapping_find('aaaaa', '') == 0
    assert count_overlapping_find('', 'a') == 0
    assert count_overlapping_find('', '') == 0

    # Test with regex too
    assert count_overlapping_regex('aaaa', 'aa') == 3
    assert count_overlapping_regex('banana', 'ana') == 2
    assert count_overlapping_regex('aaaaa', 'aa') == 4
    assert count_overlapping_regex('abcde', 'f') == 0
    assert count_overlapping_regex('aaaaa', '') == 0
    assert count_overlapping_regex('', 'a') == 0
    assert count_overlapping_regex('', '') == 0

    print("All basic tests passed!")

if __name__ == "__main__":
    test()

    # Benchmark
    haystack_size = 1_000_000
    haystack = 'a' * haystack_size
    needle = 'aa'

    print(f"Benchmarking with haystack size {haystack_size} and needle '{needle}'")

    start = time.time()
    res1 = count_overlapping_find(haystack, needle)
    end = time.time()
    print(f"count_overlapping_find: {res1}, time: {end - start:.4f}s")

    start = time.time()
    res2 = count_overlapping_regex(haystack, needle)
    end = time.time()
    print(f"count_overlapping_regex: {res2}, time: {end - start:.4f}s")

    assert res1 == res2
