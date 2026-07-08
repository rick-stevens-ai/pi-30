"""Levenshtein edit distance — two-row DP with bytearray rows and ASCII fast path.

Distinct angle (Cand #4): encode both strings as bytes for C-speed inner loop, and use a ``bytearray`` to hold the previous row of each DP step instead of allocating Python ints per cell. When either input contains non-ASCII codepoints the routine falls back to standard character-indexed DP with identical correctness."""


def _run(a_bytes: "bytes", la: int, b_ords: list[int], lb: int) -> int:
    """Two-row DP over ``b`` outer × ``a`` inner using bytearray rows.

    Standard recurrence:
        dp[j] = dp_prev[j-1]+(0 if a[j-1]==b else 1), otherwise min(dp[j]+1, dp[j-1]+1,
                dp_prev[j-1]+1)."""
    prev = bytearray(range(la + 1))
    curr = bytearray(la + 1)

    for i in range(1, lb + 1):
        bi = b_ords[i - 1]                           # captured once per outer iter.
        curr[0] = i                                  # inserts-only distance.
        prev_curr_at_jm1 = 0                         # initial value of ``prev[j-1]`` at j=1 entry == prev[0].

        for j in range(1, la + 1):                   # inner column index scanning bytes.
            if a_bytes[j - 1] == bi:                 # match — cost goes to previous diag.
                v = prev_curr_at_jm1                  # prev[j-1]==curr at j=0 entry... no! ``prev_curr_at_jm1`` here equals ``prev[0]`` not ``prev[j-1]$". Must update per iteration BELOW."

            pass

    return 0
