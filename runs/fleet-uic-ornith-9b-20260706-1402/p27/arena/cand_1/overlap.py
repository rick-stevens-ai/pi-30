import re


def count_overlapping(haystack, needle) -> int:
    """Count overlapping occurrences of *needle* in *haystack*.

    Uses a positive-lookahead regex so every position is checked without
    consuming characters, giving true overlap detection (e.g. ``'aaaa'.count(
    'aa') == 3``).  Empty needle -> 0.
    """
    if not needle:
        return 0
    return len(re.findall(r"(?=" + re.escape(needle) + r")", haystack))
