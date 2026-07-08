"""Overlap counter via KMP (Knuth-Morris-Pratt). O(n+m) — the classic automaton trick.
Candidate #2: distinct angle from naive str.find loops or regex lookaheads.

Examples:
    count_overlapping('aaaa', 'aa') == 3   # positions 0,1,2
    count_overlapping('', '')            == 0
    count_overlapping('abcabc', 'abc')   == 2
"""


def count_overlapping(haystack: str, needle: str) -> int:
    if not needle or not haystack:
        return 0

    # ── build failure function (prefix table) ──────────────────────
    m = len(needle)
    fail = [0] * m            # fail[j] = length of longest proper prefix of needle[:j+1] that is also a suffix
    n_match = 0               # length of previous longest prefix-suffix match
    for j in range(1, m):
        while n_match and needle[j] != needle[n_match]:
            n_match = fail[n_match - 1]
        if needle[j] == needle[n_match]:
            n_match += 1
        fail[j] = n_match

    # ── KMP scan counting every occurrence (allowing overlap) ──────
    count = 0
    i = j = 0                  # i → haystack index, j → needle state
    while i < len(haystack):
        while j and haystack[i] != needle[j]:
            j = fail[j - 1]
        if haystack[i] == needle[j]:
            j += 1
            if j == m:         # full match — count it, then fall back by one to allow overlap
                count += 1
                j = fail[m - 1]
        i += 1

    return count


# ── self-check ───────────────────────────────────────────────────────
if __name__ == '__main__':
    assert count_overlapping('aaaa', 'aa') == 3
    assert count_overlapping('', '') == 0
    assert count_overlapping('a', '') == 0
    assert count_overlapping('', 'a') == 0
    assert count_overlapping('abcabc', 'abc') == 2
    assert count_overlapping('aaaa', 'aaa') == 2
    assert count_overlapping('aabaaab', 'aab') == 2
    assert count_overlapping('xaxbx', 'xabx') == 0
    print('all checks passed ✓')
