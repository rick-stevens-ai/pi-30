"""Levenshtein edit distance — two-row DP, transposed for cache, early-out."""


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    la, lb = len(a), len(b)

    # Early exit against empty string
    if la == 0:
        return lb
    if lb == 0:
        return la

    # Transpose: iterate over shorter dimension as inner loop for locality
    if la < lb:
        a, b = b, a
        la, lb = lb, la

    # prev row initialises to 0..lb (insertion costs along b-axis)
    prev = list(range(lb + 1))
    curr = [0] * (lb + 1)

    for i in range(1, la + 1):
        curr[0] = i                                    # deletion cost down a-axis
        ai = ord(a[i - 1])
        for j in range(lb):
            cost = 0 if ai == ord(b[j]) else 1
            # min of left (sub), up (del), diag (match/ins)
            v_left = curr[j] + 1
            v_up = prev[j + 1] + 1
            v_diag = prev[j] + cost
            c = v_diag if v_diag <= v_left else v_left
            curr[j + 1] = c if c <= v_up else v_up
        # Quick min check — if entire row ≥ la we can't improve below that,
        # but in Python the cost of scanning outweighs benefit for typical sizes
        prev, curr = curr, prev

    return prev[lb]


if __name__ == "__main__":
    # smoke tests
    assert levenshtein("", "") == 0
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("", "abc") == 3
    assert levenshtein("abc", "") == 3
    assert levenshtein("a", "a") == 0
    assert levenshtein("abc", "abc") == 0
    print("all in-memory tests passed ✓")
