def count_overlapping(haystack: str, needle: str) -> int:
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
        start = idx + 1  # allow overlap
    return count
