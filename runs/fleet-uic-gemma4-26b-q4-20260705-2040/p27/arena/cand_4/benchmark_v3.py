import time
import re

def count_overlapping_find(haystack, needle):
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

def count_overlapping_regex_findall(haystack, needle):
    if not needle:
        return 0
    pattern = f'(?={re.escape(needle)})'
    return len(re.findall(pattern, haystack))

def count_overlapping_regex_finditer(haystack, needle):
    if not needle:
        return 0
    pattern = re.compile(f'(?={re.escape(needle)})')
    return sum(1 for _ in pattern.finditer(haystack))

def test():
    test_cases = [
        ('aaaa', 'aa', 3),
        ('banana', 'ana', 2),
        ('aaaaa', 'aa', 4),
        ('abcde', 'f', 0),
        ('aaaaa', '', 0),
        ('', 'a', 0),
        ('', '', 0),
        ('ababa', 'aba', 2),
        ('aaaaaaaaaa', 'aaa', 8),
    ]
    
    for haystack, needle, expected in test_cases:
        assert count_overlapping_find(haystack, needle) == expected, f"Failed find: {haystack}, {needle}"
        assert count_overlapping_regex_findall(haystack, needle) == expected, f"Failed regex findall: {haystack}, {needle}"
        assert count_overlapping_regex_finditer(haystack, needle) == expected, f"Failed regex finditer: {haystack}, {needle}"

    print("All basic tests passed!")

if __name__ == "__main__":
    test()

    # Benchmark 1: Small needle, large haystack (lots of matches)
    haystack_size = 1_000_000
    haystack = 'a' * haystack_size
    needle = 'aa'

    print(f"\nBenchmark 1: Haystack size {haystack_size}, needle '{needle}' (many matches)")

    start = time.time()
    res1 = count_overlapping_find(haystack, needle)
    end = time.time()
    print(f"count_overlapping_find: {res1}, time: {end - start:.4f}s")

    start = time.time()
    res2 = count_overlapping_regex_findall(haystack, needle)
    end = time.time()
    print(f"count_overlapping_regex_findall: {res2}, time: {end - start:.4f}s")

    start = time.time()
    res3 = count_overlapping_regex_finditer(haystack, needle)
    end = time.time()
    print(f"count_overlapping_regex_finditer: {res3}, time: {end - start:.4f}s")

    assert res1 == res2 == res3

    # Benchmark 2: Long needle, large haystack (few matches)
    needle = 'a' * 100 + 'b'
    haystack = ('a' * 100 + 'b') * 10000
    print(f"\nBenchmark 2: Haystack size {len(haystack)}, needle length {len(needle)} (few matches)")

    start = time.time()
    res1 = count_overlapping_find(haystack, needle)
    end = time.time()
    print(f"count_overlapping_find: {res1}, time: {end - start:.4f}s")

    start = time.time()
    res2 = count_overlapping_regex_findall(haystack, needle)
    end = time.time()
    print(f"count_overlapping_regex_findall: {res2}, time: {end - start:.4f}s")

    start = time.time()
    res3 = count_overlapping_regex_finditer(haystack, needle)
    end = time.time()
    print(f"count_overlapping_regex_finditer: {res3}, time: {end - start:.4f}s")

    assert res1 == res2 == res3

    # Benchmark 3: No matches
    haystack = 'a' * haystack_size
    needle = 'b'
    print(f"\nBenchmark 3: Haystack size {haystack_size}, needle 'b' (no matches)")

    start = time.time()
    res1 = count_overlapping_find(haystack, needle)
    end = time.time()
    print(f"count_overlapping_find: {res1}, time: {end - start:.4f}s")

    start = time.time()
    res2 = count_overlapping_regex_findall(haystack, needle)
    end = time.time()
    print(f"count_overlapping_regex_findall: {res2}, time: {end - start:.4f}s")

    start = time.time()
    res3 = count_overlapping_regex_finditer(haystack, needle)
    end = time.time()
    print(f"count_overlapping_regex_finditer: {res3}, time: {end - start:.4f}s")

    assert res1 == res2 == res3
