def count_overlapping(haystack: str, needle: str) -> int:
    """Return number of overlapping occurrences of needle in haystack.
    Empty needle returns 0.
    Runs in O(len(haystack)) using a sliding window approach.
    """
    if not needle:
        return 0
    count = 0
    start = 0
    while True:
        pos = haystack.find(needle, start)
        if pos == -1:
            break
        count += 1
        start = pos + 1
    return count