import time
import re

def count_overlapping_find(haystack: str, needle: str) -> int:
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

def count_overlapping_re(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    # Using findall with lookahead. Match is zero-width, so it finds all starting positions.
    return len(re.findall(f'(?={re.escape(needle)})', haystack))

def benchmark(name, func, haystack, needle):
    start_time = time.time()
    res = func(haystack, needle)
    end_time = time.time()
    print(f"{name:10} | matches: {res:<8} | time: {end_time - start_time:.6f}s")
    return res

def run_benchmarks():
    scenarios = [
        ("Dense 'a'", lambda: ('a' * 1_000_000, 'aa')),
        ("Sparse 'a'", lambda: ('abcde' * 200_000, 'abcde')),
        ("Long needle", lambda: ('a' * 1_000_000, 'a' * 500_000)),
        ("No match", lambda: ('abcdefg', 'xyz')),
    ]

    for name, setup in scenarios:
        print(f"--- Scenario: {name} ---")
        haystack, needle = setup()
        res_find = benchmark("find", count_overlapping_find, haystack, needle)
        res_re = benchmark("re", count_overlapping_re, haystack, needle)
        assert res_find == res_re
        print()

if __name__ == "__main__":
    run_benchmarks()
