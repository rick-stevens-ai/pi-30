"""Count overlapping substring occurrences using the KMP automaton."""

from typing import SupportsIndex


def count_overlapping(haystack: str, needle: str) -> int:
    """Return the number of *overlapping* occurrences of *needle* in *haystack*.

    Examples
    --------
    >>> count_overlapping('aaaa', 'aa')
    3
    >>> count_overlapping('abababa', 'aba')
    3
    >>> count_overlapping('hello', '')
    0

    Runs in O(len(haystack) + len(needle)) time and O(len(needle)) space
    via the KMP failure-function automaton — no backtracking, no Python
    loop overhead for the inner match test.
    """
    if not needle or len(needle) > len(haystack):
        return 0

    # --- build KMP failure function (prefix table) ---
    # fail[j] = length of the longest proper prefix of needle[:j+1]
    # that is also a suffix of needle[:j+1].
    m = len(needle)
    fail = [0] * m
    k = 0
    for j in range(1, m):
        while k > 0 and needle[k] != needle[j]:
            k = fail[k - 1]
        if needle[k] == needle[j]:
            k += 1
        fail[j] = k

    # --- scan haystack with the KMP automaton ---
    count = 0
    q = 0  # number of characters matched so far
    for ch in haystack:
        while q > 0 and needle[q] != ch:
            q = fail[q - 1]
        if needle[q] == ch:
            q += 1
        if q == m:
            count += 1
            q = fail[q - 1]  # allow overlap: resume from longest border

    return count
