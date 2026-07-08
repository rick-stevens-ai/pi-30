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

def test_performance():
    haystack = 'a' * 1_000_000
    needle = 'aa'
    
    print(f"Haystack size: {len(haystack)}")
    
    start_time = time.time()
    res_find = count_overlapping_find(haystack, needle)
    end_time = time.time()
    print(f"find: {res_find} matches in {end_time - start_time:.4f}s")

    start_time = time.time()
    res_re = count_overlapping_re(haystack, needle)
    end_time = time.time()
    print(f"re:   {res_re} matches in {end_time - start_time:.4f}s")

    assert res_find == res_re == 999999

if __name__ == "__main__":
    test_performance()
