"""Count overlapping (not just str.count) occurrences of needle in haystack.

Empty needle -> 0 (by contract).
Fast on long strings: delegate the scanning to a single compiled regex using a
lookahead so matches don't consume input, allowing overlaps. The regex engine
runs in C and is dramatically faster than a Python-level find loop on big input.
"""

import re
from functools import lru_cache


@lru_cache(maxsize=512)
def _pattern(needle: str) -> "re.Pattern[str]":
    # Lookahead = match without consuming, so occurrences can overlap.
    # re.escape keeps arbitrary needle text literal (regex metachars safe).
    return re.compile("(?=" + re.escape(needle) + ")")


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of OVERLAPPING occurrences of needle in haystack.

    count_overlapping('aaaa', 'aa') == 3  (str.count would give 2).
    count_overlapping('abc',   '')   == 0  (empty needle contract).
    """
    if not needle:  # empty needle -> 0, also avoids infinite-match regex
        return 0
    if not haystack or len(needle) > len(haystack):
        return 0
    # finditer returns one match object per overlapping hit; iterate to count.
    # Using sum over a generator avoids building a list for long strings.
    pat = _pattern(needle)
    return sum(1 for _ in pat.finditer(haystack))


if __name__ == "__main__":
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("abc", "") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("aaa", "a") == 3
    assert count_overlapping("ababab", "ab") == 3
    assert count_overlapping("abcabc", "abc") == 2
    assert count_overlapping("xxxx", "xx") == 3
    assert count_overlapping("hello.world", ".") == 1  # regex metachar
    assert count_overlapping("a+a+", "a+") == 2          # regex metachar
    assert count_overlapping("nope", "z") == 0
    print("ok")
