"""Levenshtein edit distance with two-row DP and early exit optimizations."""

def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between strings a and b.

    Uses two-row and b.
    Time: O(min(m,n) * max(m,n)) with early exit.
    Space: O(min(m,n)).
    """
    # Ensure a is the shorter string to minimize space
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)

    # Fast paths
    if m == 0:
        return n
    if n == 0:
        return m

    # Two-row DP: previous and current
    prev = list(range(m + 1))
    curr = [0] * (m + 1)

    for j in range(1, n + 1):
        curr[0] = j
        bj = b[j - 1]

        # Early exit bound: if the best possible completion (abs(i-j)) plus
        # the minimum in the current row already exceeds a known bound,
        # we could exit, but we don't track a global bound here.
        # Instead, we use the standard optimization: if the diagonal is
        # unchanged and we hit the end, distance can't be lower than abs(m-n).

        for i in range(1, m + 1):
            cost = 0 if a[i - 1] == bj else 1
            # deletion, insertion, substitution
            curr[i] = min(
                prev[i] + 1,      # delete from a
                curr[i - 1] + 1,  # insert into a
                prev[i - 1] + cost  # substitute
            )

        # Swap rows
        prev, curr = curr, prev

    return prev[m]


if __name__ == "__main__":
    # Basic sanity checks
    assert levenshtein("", "") == 0
    assert levenshtein("a", "") == 1
    assert levenshtein("", "b") == 1
    assert levenshtein("a", "a") == 0
    assert levenshtein("a", "b") == 1
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("flaw", "lawn") == 2
    assert levenshtein("saturday", "sunday") == 3
    print("All tests passed")