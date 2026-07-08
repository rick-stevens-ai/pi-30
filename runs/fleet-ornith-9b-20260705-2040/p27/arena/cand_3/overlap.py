"""Count overlapping occurrences of *needle* in *haystack*.

Uses ``str.find`` (C-level Boyer–Moore-Horspool) advancing one byte at a time
after each hit, so matches may overlap.  Empty needle or needle longer than
haystack yields ``0``.
"""


def count_overlapping(haystack: str, needle: str) -> int:
    if not needle or len(needle) > len(haystack):
        return 0

    n = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break
        n += 1
        start = idx + 1  # advance only one byte to allow overlap
    return n
