"""Overlap finder — KMP-based overlapping occurrence counter (stdlib only).

Counts how many times ``needle`` appears in ``haystack``, including
overlapping matches.  Unlike *str.count* which consumes the haystack
between each match, we advance by a single character on every failure,
giving true O(len(haystack)) worst-case time — no matter what the
input looks like.

    >>> count_overlapping('aaaa', 'aa')
    3

Edge cases handled: empty needle → 0, needle longer than haystack → 0.
"""

def count_overlapping(haystack: str, needle: str) -> int:
    if not needle or not haystack or len(needle) > len(haystack):
        return 0

    # ── Build the KMP prefix (failure) function ────────────────────────
    m = len(needle)
    fail = [0] * m                       # fail[i] = length of longest
                                         #     proper prefix of needle[:i+1]
                                         #     that is also a suffix
    for i in range(1, m):
        j = fail[i - 1]                  # follow the chain
        while j and needle[i] != needle[j]:
            j = fail[j - 1]
        if needle[i] == needle[j]:
            j += 1
        fail[i] = j

    # ── KMP scan over haystack, advancing by ONE column on each step ──
    count = 0
    n_haystack = len(haystack)
    j = 0                                # current position in needle

    for i in range(n_haystack):                                  # ← O(N)
        c = haystack[i]
        while j and needle[j] != c:      # walk back along failure chain
            j = fail[j - 1]
        if needle[j] == c:
            j += 1

        if j == m:                       # full match found!
            count += 1
            j = fail[m - 1]              # shift by the longest safe prefix
                                         #     (enables overlapping re-detect)

    return count
