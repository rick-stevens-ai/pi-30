def count_overlapping(haystack, needle):
    """Count overlapping occurrences of needle in haystack.

    Uses str.find (C-level search) to skip ahead efficiently, then advances
    by 1 after each match to allow overlaps. Empty needle returns 0.
    """
    if not needle:
        return 0
    n = len(haystack)
    m = len(needle)
    count = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count
