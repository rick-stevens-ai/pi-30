def count_overlapping(haystack: str, needle: str) -> int:
    """
    Count the number of overlapping occurrences of `needle` in `haystack`.
    Empty needle returns 0. Uses efficient sliding window.
    Examples: 'aa' in 'aaaa' is 3, not 2 as with(str).count().
    """
    if not needle:
        return 0
    n_len, h_len = len(needle), len(haystack)
    if n_len > h_len or n_len == 0:
        return 0

    # Precompute the prefix function (KMP style) to find longest proper prefix which is also suffix
    prefix = [0] * n_len
    for i in range(1, n_len):
        j = prefix[i - 1]
        while j > 0 and needle[i] != needle[j]:
            j = prefix[j - 1]
        if needle[i] == needle[j]:
            j += 1
        prefix[i] = j

    count = 0
    j = 0  # current position in needle
    for i, c in enumerate(haystack):
        while j > 0 and c != needle[j]:
            j = prefix[j - 1]
        if c == needle[j]:
            j += 1
        if j == n_len:
            count += 1
            # After match, continue with next character immediately (overlap)
            # Use the full-length prefix entry to start matching for overlaps
            j = n_len
    return count
