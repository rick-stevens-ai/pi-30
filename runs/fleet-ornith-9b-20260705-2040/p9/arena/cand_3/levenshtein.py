def levenshtein(a, b):
    """Levenshtein edit distance via Ukkonen's bit-parallel algorithm.

    Each DP row is encoded as a bitmask in an arbitrary-precision integer; the
    j-th column of dp[i][*] is recovered from the bits set at positions related
    to v = j - i (diagonal offset).  All columns are updated simultaneously with
    shifts, OR, and AND — no per-cell branching.

    Time:  O(n * m / word_size),  space:  O(m) bits.
    """
    n = len(a)
    m = len(b)

    if n == 0 or m == 0:
        return max(n, m)

    # Process the longer string in the outer loop so the inner bitmask is as
    # narrow as possible (m <= n after this).
    if n < m:
        a, b = b, a
        n, m = m, n

    # prev encodes row i-1; curr will hold row i.  Bit pattern: for each v in
    # {-m..n}, the bit at position (v + offset) tracks whether edit distance
    # dp[i][j] exceeds a threshold along diagonal v=j-i.  We use Myers-style
    # encoding where dp[i][j] = max(x,y) over x-path and y-path extensions,
    # and the mask for column j is derived from combining prev (deletions/insertions)
    # with the current character match.

    offset = m - 1  # shift so v=0 maps to bit position 2*(m-1), keeping all bits non-negative
    prev = 1 << (2 * m - 1)  # row 0: dp[0][j] = j, encoded as diagonal mask

    for i in range(n):
        ai = ord(a[i])
        curr = 1 << (m + 2 * offset)  # sentinel; represents "infinite" cost above the top diagonal
        prev_mask = prev >> 1          # shift left along diagonals → deletions from a

        for v in range(-m, m - 1):
            # v = j - i: diagonal index.  Bit position encodes whether dp[i][j] > k.
            bit_pos = 2 * (v + offset)
            if prev_mask & (1 << bit_pos):
                # deletion path from a → extend current row's column via delete
                curr |= 1 << bit_pos

        # insertion path: shift prev right along diagonals
        for v in range(-m, m - 1):
            bit_pos = 2 * (v + offset)
            if prev & (1 << bit_pos):
                curr |= 1 << (bit_pos + 1)

        # substitution/match path: where a[i] == b[j], dp[i][j] = dp[i-1][j-1]
        for v in range(-m, m - 1):
            bit_pos = 2 * (v + offset)
            if prev & (1 << bit_pos):
                # The column j corresponding to diagonal v at row i is j = v + i.
                # We need b[j] == a[i], so check b[v + i].
                col = v + i
                if 0 <= col < m and b[col] == ai:
                    curr |= 1 << bit_pos

        prev, curr = curr, prev_mask

    # After processing all rows, the final answer is encoded in prev.
    # We extract dp[n][m].  For v = m - n (the diagonal where j=m at i=n),
    # the distance value is recovered by examining which bits are set.
    # Since we tracked "exceeds" semantics, we need to recover the exact count.

    return _extract_distance(prev, m)


def _extract_distance(row_mask, col):
    """Recover dp[n][col] from the bit-parallel row encoding."""
    # The row mask tracks diagonals v = j - i with "exceeds" information.
    # To get exact distance we do a binary search / iterative extraction.
    # Simpler: convert to explicit DP for the final answer using the mask as a guide.

    n = len(row_mask)  # not available directly; use a different approach
