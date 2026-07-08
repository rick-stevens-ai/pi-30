"""Fast two-row DP Levenshtein distance with short-pass early exits."""


def levenshtein(a: str, b: str) -> int:
    """Return the edit (Levenshtein) distance between strings *a* and *b*.

    Uses a two-row dynamic programme.  When one operand is much shorter than
    the other we also bail out early as soon as the cheapest possible
    completion exceeds what we have already found - a tiny but real speed-up
    on pathological mismatched inputs.
    """
    # Swap so the shorter string drives column work (less scratch space).
    if len(b) < len(a):
        a, b = b, a

    m: int = len(a)
    n: int = len(b)

    # --- trivial cases ---------------------------------------------------
    if m == 0:
        return n

    if a == b:
        return 0

    # --- two-row DP -----------------------------------------------------
    row_one = list(range(m + 1))   # previous (top) row
    row_two = [0] * (m + 1)         # current (running) row

    for j in range(1, n + 1):
        b_j_1 = a[j - 1]            # cache lookup to avoid repeated indexing
        row_two[0] = j              # deletion cost at column zero

        best_for_this_row = j       # track minimum inside this row (early exit)

        for i in range(1, m + 1):
            if b_j_1 == a[i - 1]:   # no edit needed: copy diagonal
                c = row_one[i - 1]
            else:                    # min of delete / insert / sub + 1
                best = row_one[i]    # deletion
                ins_cost = row_two[i - 1]   # insertion along this row
                if ins_cost < best:
                    best = ins_cost
                diag = row_one[i - 1]     # substitution
                if diag < best:
                    best = diag

            c = best + 1
            row_two[i] = c
            if c < best_for_this_row:
                best_for_this_row = c

        # --- early exit (lower bound) ---------------------------------
        # remaining `n - j` rows each need at least one insertion to fill
        # the missing columns; so any partial distance here is >= some lower
        # bound already exceeded.  This is safe for every standard metric.
        if best_for_this_row > n:
            break

        row_one, row_two = row_two[:], row_one[:]

    return row_one[m]
