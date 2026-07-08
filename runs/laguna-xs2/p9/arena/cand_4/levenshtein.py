"""Levenshtein edit distance with two-row DP and early exit optimizations."""


def levenshtein(a: str, b: str) -> int:
    """Return the minimum number of single-character edits (insertions,
    deletions, substitutions) required to transform string a into string b.

    Uses two-row dynamic programming for O(min(m,n)) space and includes
    early exit optimizations for common cases.
    """
    # Early exit: identical strings
    if a is b or a == b:
        return 0

    # Ensure a is the longer string (outer loop), b is shorter (inner loop)
    if len(a) < len(b):
        a, b = b, a

    # Early exit: empty string
    if not b:
        return len(a)

    m, n = len(a), len(b)

    # Two rows: previous and current
    # prev[j] = distance for a[0..i-1] to b[0..j-1]
    # cur[j] = distance for a[0..i] to b[0..j-1]
    prev = list(range(n + 1))
    cur = [0] * (n + 1)

    for i in range(1, m + 1):
        cur[0] = i

        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(cur[j - 1],  # insertion
                                 prev[j],      # deletion
                                 prev[j - 1])  # substitution

        # Swap rows: move current to previous for next iteration
        prev, cur = cur, prev

    # After the loop, prev holds the last computed row
    return prev[n]