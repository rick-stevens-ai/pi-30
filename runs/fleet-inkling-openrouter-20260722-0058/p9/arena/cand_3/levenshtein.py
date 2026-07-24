def levenshtein(a: str, b: str) -> int:
    """Edit distance using two-row DP with early exit."""
    if a == b:
        return 0
    len_a, len_b = len(a), len(b)
    # Ensure a is shorter for less memory / fewer ops
    if len_a > len_b:
        a, b = b, a
        len_a, len_b = len_b, len_a
    # Early exit if one is empty
    if len_a == 0:
        return len_b

    prev = list(range(len_a + 1))
    curr = [0] * (len_a + 1)
    for j in range(1, len_b + 1):
        curr[0] = j
        b_char = b[j - 1]
        min_curr = curr[0]
        for i in range(1, len_a + 1):
            cost = 0 if a[i - 1] == b_char else 1
            val = min(
                curr[i - 1] + 1,      # delete
                prev[i] + 1,          # insert
                prev[i - 1] + cost    # substitute
            )
            curr[i] = val
            if val < min_curr:
                min_curr = val
        # Early exit: if min in row exceeds best possible, break
        # (kept simple; two-row is already fast)
        prev, curr = curr, prev
    return prev[len_a]
