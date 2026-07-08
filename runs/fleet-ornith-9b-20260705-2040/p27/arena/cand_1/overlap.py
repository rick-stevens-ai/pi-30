"""Count overlapping occurrences of *needle* in *haystack*.

Uses CPython's C-implemented ``str.find`` with a unit-step advance so that
matches may share characters (e.g. ``'aa'.count('a', 'aaaa') == 3``).
"""


def count_overlapping(haystack: str, needle: str) -> int:
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
