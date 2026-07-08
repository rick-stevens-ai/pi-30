"""Utility to count overlapping occurrences of a needle within a haystack.

The implementation uses only the Python standard library and runs efficiently
by leveraging str.find in a loop that advances only one character after each
match, thus preserving overlap semantics.

Example:
    >>> count_overlapping('aaaa', 'aa')
    3
    >>> count_overlapping('abcabc', 'aba')
    1
    >>> count_overlapping('hello', '')
    0
"""

def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return the number of (possibly overlapping) occurrences of *needle* in
    *haystack*.

    Args:
        haystack: The string to search within.
        needle:   The pattern to look for.

    Returns:
        An integer count.  Zero is returned if ``needle`` is empty.

    Notes:
        Overlapping matches are counted, i.e. searching for "aa" in
        "aaaa" yields 3 matches (positions 0‑1, 1‑2, and 2‑3).
    """
    # Fast‑path: an empty needle cannot produce any meaningful match.
    if not needle:
        return 0

    count = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        count += 1
        # Move just one character forward to allow overlapping matches.
        start = idx + 1
    return count

# The following block enables the module to be executed directly for quick testing.
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        prog = sys.argv[0]
        print(f"Usage: {prog} <haystack> <needle>", file=sys.stderr)
        sys.exit(1)

    hay, needle = sys.argv[1], sys.argv[2]
    result = count_overlapping(hay, needle)
    print(result)