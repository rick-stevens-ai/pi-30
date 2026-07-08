def levenshtein(a, b):
    \"\""
    Compute the Levenshtein edit distance between strings `a` and `b`.

    Returns:
        int: The minimum number of single-character edits (insertions,
        deletions, or substitutions) required to change `a` into `b`.

    This implementation uses a two-row dynamic programming approach
    which is optimal for speed while using only O(min(len(a), len(b))) 
    additional memory.
    \"\"\"
    # Quick cases
    if a == b:
        return 0

    n, m = len(a), len(b)

    # Ensure the shorter string drives the inner loop to minimize work.
    # If b is longer, swap so that `m` is the smaller dimension.
    swapped = False
    if m > n:
        a, b = b, a
        n, m = m, n
        swapped = True

    # `prev` is a list representing distances for the previous row.
    prev = list(range(m + 1))

    # Iterate over each character of the longer string `a`
    for i in range(1, n + 1):
        curr = [i] + [0] * m
        ai = a[i - 1]

        # Populate current row using two previous values:
        # prev[j]   -> distance without current char (deletion)
        # curr[j-1] -> distance with current inserted char (insertion)
        # prev[j-1] + cost -> substitution / match
        for j in range(1, m + 1):
            cost = 0 if ai == b[j - 1] else 1
            curr[j] = min(prev[j] + 1,       # deletion
                          curr[j - 1] + 1,     # insertion
                          prev[j - 1] + cost)  # substitution

        # Early exit optimization: if the smallest possible remaining distance
        # (assuming all remaining chars are deletions/insertions) already exceeds
        # a previously found lower bound, we could break. However, for simplicity
        # and correctness across all input sizes we keep the loop intact.
        prev = curr

    return prev[m]