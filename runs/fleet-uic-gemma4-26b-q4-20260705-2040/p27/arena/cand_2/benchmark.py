import time
import re

def count_overlapping_find(haystack, needle):
    if not needle:
        return 0
    count = 0
    pos = haystack.find(needle)
    while pos != -1:
        count += 1
        pos = haystack.find(needle, pos + 1)
    return count

def count_overlapping_re_findall(haystack, needle):
    if not needle:
        return 0
    return len(re.findall(f'(?={re.escape(needle)})', haystack))

def count_overlapping_re_finditer(haystack, needle):
    if not needle:
        return 0
    return sum(1 for _ in re.finditer(f'(?={re.escape(needle)})', haystack))

# Benchmark
haystack = "a" * 10**6
needle = "aa"

start = time.time()
res_find = count_overlapping_find(haystack, needle)
end = time.time()
print(f"Find: {res_find}, time: {end - start:.4f}s")

start = time.time()
res_re_findall = count_overlapping_re_findall(haystack, needle)
end = time.time()
print(f"Regex Findall: {res_re_findall}, time: {end - start:.4f}s")

start = time.time()
res_re_finditer = count_overlapping_re_finditer(haystack, needle)
end = time.time()
print(f"Regex Finditer: {res_re_finditer}, time: {end - start:.4f}s")

# Test correctness
assert count_overlapping_find("aaaa", "aa") == 3
assert count_overlapping_re_findall("aaaa", "aa") == 3
assert count_overlapping_re_finditer("aaaa", "aa") == 3

assert count_overlapping_find("a.b.c", ".") == 2
assert count_overlapping_re_findall("a.b.c", ".") == 2
assert count_overlapping_re_finditer("a.b.c", ".") == 2

print("All tests passed!")
