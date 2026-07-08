"""Overlap-counting — Candidate #3: regex-lookahead (distinct from brute-force / str.count approaches)."""

import re


def count_overlapping(haystack: "str", needle: "str") -> int:
    """Return the number of *overlapping* occurrences of ``needle`` in ``haystack``.

    An empty or longer-than-haystack needle always returns 0.
    Uses a *look-ahead* regex so matches do not consume characters, allowing adjacent positions to all be counted.

    >>> count_overlapping("aaaa", "aa")
    3
    >>> count_overlapping("", "")
    0
    >>> count_overlapping("abcabc", "abc")
    2
    >>> count_overlapping("aaa", "b")
    0
    >>> count_overlapping("ababa", "a")
    3
    """

    if not needle:
        return 0
    # The '(?=...)' lookahead matches at every position where the literal appears
    # *without consuming* characters — so overlapping hits are each detected separately.
    pattern = '(?=' + re.escape(needle) + ')'
    compiled = _CACHE.get(pattern)
    if compiled is None:
        compiled = re.compile(pattern)
        _CACHE[pattern] = compiled

    count = 0
    for _ in compiled.finditer(haystack):
        count += 1          # fast — finditer itself walks the haystack only via C code paths internally
    return count


# Module-level cache of pre-compiled pattern so repeated calls with the same needle
# skip re.escape + compile (costs avoided on hot loops while still being stdlib-only).
_CACHE: dict[str, "re.Pattern"] = {}
