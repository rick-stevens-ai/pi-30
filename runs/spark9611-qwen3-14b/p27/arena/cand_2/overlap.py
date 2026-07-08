def count_overlapping(haystack, needle):
    if not needle:
        return 0
    count = 0
    start = 0
    len_needle = len(needle)
    len_haystack = len(haystack)
    if len_needle > len_haystack:
        return 0
    while True:
        pos = haystack.find(needle, start)
        if pos == -1:
            break
        count += 1
        start = pos + 1
    return count