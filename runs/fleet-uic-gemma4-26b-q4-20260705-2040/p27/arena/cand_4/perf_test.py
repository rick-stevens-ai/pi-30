import time

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

def count_overlapping_regex(haystack, needle):
    import re
    if not needle:
        return 0
    pattern = f'(?={re.escape(needle)})'
    return len(re.findall(pattern, haystack))

def test_perf():
    # Case 1: Many matches (all 'a')
    h1 = 'a' * 1_000_000
    n1 = 'aa'
    print("Case 1 (Many matches):")
    t0 = time.time()
    r1 = count_overlapping_find(h1, n1)
    t1 = time.time()
    print(f"  find: {t1-t0:.4f}s, res={r1}")
    
    t0 = time.time()
    r2 = count_overlapping_regex(h1, n1)
    t1 = time.time()
    print(f"  regex: {t1-t0:.4f}s, res={r2}")

    # Case 2: Few matches
    h2 = ('a' * 100 + 'b') * 10_000
    n2 = 'a' * 100 + 'b'
    print("\nCase 2 (Few matches):")
    t0 = time.time()
    r1 = count_overlapping_find(h2, n2)
    t1 = time.time()
    print(f"  find: {t1-t0:.4f}s, res={r1}")
    
    t0 = time.time()
    r2 = count_overlapping_regex(h2, n2)
    t1 = time.time()
    print(f"  regex: {t1-t0:.4f}s, res={r2}")

    # Case 3: No matches
    h3 = 'a' * 1_000_000
    n3 = 'b'
    print("\nCase 3 (No matches):")
    t0 = time.time()
    r1 = count_overlapping_find(h3, n3)
    t1 = time.time()
    print(f"  find: {t1-t0:.4f}s, res={r1}")
    
    t0 = time.time()
    r2 = count_overlapping_regex(h3, n3)
    t1 = time.time()
    print(f"  regex: {t1-t0:.4f}s, res={r2}")

if __name__ == "__main__":
    test_perf()
