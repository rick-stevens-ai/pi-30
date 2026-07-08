"""Count overlapping occurrences of needle in haystack.

Distinct angle: leverage C-level regex lookahead to iterate all start positions
without consuming characters — fast on long strings, stdlib only.
"""

import re


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of overlapping occurrences of *needle* in *haystack*.

        'aaaa'[0] and [1] and [2], but NOT at index 3 which would need a
        second 'a' — that is why ``count_overlapping("aaaa", "aa") == 3``.

    An empty needle returns 0 regardless of the haystack.
    """
    if not needle:
        return 0

    # (?=...) is a zero-width positive lookahead — the engine tries to match at
    # every position and does NOT consume characters, so 'aa' is found in
    # positions 0, 1, 2 of 'aaaa'. re.findall returns a list of the captured
    # (empty) groups for each look-ahead hit; its length equals the count.
    pattern = re.compile(f"(?={re.escape(needle)})")
    return len(pattern.findall(haystack))
