import time
import re

def count_overlapping_find(haystack, needle):
    if not needle: return 0
    count = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1: break
        count += 1
        start = idx + 1
    return count

def count_overlapping_re(haystack, needle):
    if not needle: return 0
    # Use finditer to avoid creating a large list of matches in memory
    pattern = re.compile(f'(?={re.escape(needle)})')
    return sum(1 for _ in pattern.finditer(haystack))

def count_overlapping_naive(haystack, needle):
    if not needle: return 0
    count = 0
    n = len(needle)
    for i in range(len(haystack) - n + 1):
        if haystack[i : i + n] == needle:
            count += 1
    return count

def test():
    test_cases = [
        ("aaaa", "aa", 3),
        ("aaaaa", "aa", 4),
        ("ababa", "aba", 2),
        ("banana", "ana", 2),
        ("abcde", "f", 0),
        ("abcde", "", 0),
        ("aaaaaa", "aaa", 4),
    ]

    for h, n, expected in test_cases:
        res1 = count_overlapping_find(h, n)
        res2 = count_overlapping_re(h, n)
        res3 = count_overlapping_naive(h, n)
        print(f"H='{h}', N='{n}' | Exp={expected} | Find={res1}, Re={res2}, Naive={res3}")
        assert res1 == expected and res2 == expected and res3 == expected

    # Benchmarking
    size = 10**6
    h_large = 'a' * size
    n_large = 'aa'
    expected_large = size - 1

    print(f"\nBenchmarking with haystack size {size} and needle '{n_large}'")
    
    start = time.time()
    res = count_overlapping_find(h_large, n_large)
    print(f"Find: {time.time()-start:.4f}s (result={res})")

    start = time.time()
    res = count_overlapping_re(h_large, n_large)
    print(f"Re:   {time.time()-start:.4f}s (result={res})")

    # Naive might be too slow for 10^6
    # start = time.time()
    # res = count_overlapping_naive(h_large, n_large)
    # print(f"Naive: {time.time()-start:.4f}s (result={res})")

if __name__ == "__main__":
    test()
