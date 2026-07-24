def count_overlapping(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    count = 0
    n = len(needle)
    # Find all starting positions using find in a loop
    pos = haystack.find(needle)
    while pos != -1:
        count += 1
        pos = haystack.find(needle, pos + 1)
    return count
