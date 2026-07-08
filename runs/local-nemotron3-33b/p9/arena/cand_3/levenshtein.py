def levenshtein(a: str, b: str) -> int:
    """
    Compute the Levenshtein edit distance between two strings.

    Features:
      * Handles empty strings correctly.
      * Uses O(min(len(a), len(b))) memory (two‑row DP).
      * Early exit for trivial cases (identical strings or one empty).

    Args:
        a: First string.
        b: Second string.

    Returns:
        The edit distance as an integer.
    """
    # Trivial cases with early exit
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la

    # Ensure `a` is the shorter string to minimise memory usage.
    if la > lb:
        a, b = b, a
        la, lb = lb, la

    # previous row of distances: distance from empty prefix of `b` to prefixes of `a`
    prev = list(range(la + 1))

    for i in range(1, lb + 1):
        # current row starts with cost `i` (all insertions so far)
        cur = [i] + [0] * la
        char_b = b[i - 1]

        for j in range(1, la + 1):
            cost = 0 if a[j - 1] == char_b else 1
            # three possible operations: delete, insert, substitute/match
            cur[j] = min(prev[j] + 1,          # deletion
                         cur[j - 1] + 1,       # insertion
                         prev[j - 1] + cost)   # substitution / match

        # Early exit check: if the minimal possible remaining distance is already
        # larger than what we could achieve by simply inserting/deleting the rest,
        # we can break. For simplicity and speed we skip this extra logic –
        # the two‑row DP is already optimal.
        prev = cur

    return prev[la]