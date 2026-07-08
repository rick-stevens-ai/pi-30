# Fast overlapping substring counter (stdint only)

def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return the number of overlapping occurrences of `needle` in `haystack`.

    Examples:
        count_overlapping('aaaa', 'aa') == 3  # not 2 as str.count would return.
    """
    if needle == "":
        return 0
    n_len = len(needle)
    h_len = len(haystack)

    count = 0
    for i in range(0, h_len - n_len + 1):
        if haystack[i:i+n_len] == needle:
            count += 1
    return count
