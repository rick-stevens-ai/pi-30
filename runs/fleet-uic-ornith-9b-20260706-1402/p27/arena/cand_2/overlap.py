def count_overlapping(haystack: str, needle: str) -> int:
    """Count overlapping occurrences of *needle* in *haystack*.

    Uses KMP (Knuth-Morris-Pratt) string matching so that every position
    is examined in linear time — no redundant rescanning after a partial
    match.  Empty needle → 0 by convention; longer needle than haystack
    also yields 0 immediately.
    """
    if not needle:
        return 0

    m = len(needle)
    n = len(haystack)
    if m > n:
        return 0

    # ── build KMP prefix (failure) function for the pattern ────────────
    pi = [0] * m
    k = 0
    for i in range(1, m):
        while k and needle[k] != needle[i]:
            k = pi[k - 1]
        if needle[k] == needle[i]:
            k += 1
        pi[i] = k

    # ── KMP search over the text ───────────────────────────────────────
    count = 0
    q = 0                              # number of characters matched
    for i in range(n):
        while q and needle[q] != haystack[i]:
            q = pi[q - 1]
        if needle[q] == haystack[i]:
            q += 1
        if q == m:                     # full match found at position (i-m+1)
            count += 1
            q = pi[q - 1]              # follow the failure link → allow overlap

    return count
