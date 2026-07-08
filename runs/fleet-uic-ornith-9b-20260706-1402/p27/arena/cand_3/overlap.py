def count_overlapping(haystack, needle):
    if not needle or len(needle) > len(haystack):
        return 0

    start = 0
    count = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        # Slide by one to allow overlapping matches (e.g. 'aa' in 'aaaa')
        start = idx + 1
    return count
