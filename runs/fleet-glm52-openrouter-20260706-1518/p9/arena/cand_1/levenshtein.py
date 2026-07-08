"""Levenshtein edit distance, optimized for the exact-distance case.

Candidate #1 distinct angle.

Optimizations (all sound / correctness-preserving):
  * Empty-string and identical-string short circuits.
  * Common-prefix and common-suffix trimming (reduces both dimensions).
  * Make the shorter string the inner dimension (O(min(len)) memory).
  * Two rolling rows instead of a full (m+1)x(n+1) table.
  * Local variable hoisting + avoids ``min`` builtin call overhead in the
    inner loop.

Stdlib only.
"""

from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between ``a`` and ``b``.

    Correct for all inputs, including empty strings.
    """
    la = len(a)
    lb = len(b)

    # --- Empty-string short circuits. ---
    if la == 0:
        return lb
    if lb == 0:
        return la

    # --- Identical-string short circuit (also covers a is b). ---
    if a == b:
        return 0

    # --- Trim common prefix. ---
    # Sound: aligned matching leading characters contribute 0 to the distance.
    start = 0
    a_start = a
    b_start = b
    # Compare in chunks first for speed on long common prefixes.
    lo = 0
    hi = la if la < lb else lb
    while lo < hi and a_start[lo] == b_start[lo]:
        lo += 1
    start = lo
    # Trailing slice of the prefix-stripped strings.
    a = a_start[start:]
    b = b_start[start:]
    la -= start
    lb -= start

    # --- Trim common suffix (after prefix trim, on the remaining tails). ---
    k = 0
    while k < la and k < lb and a[la - 1 - k] == b[lb - 1 - k]:
        k += 1
    if k:
        a = a[: la - k]
        b = b[: lb - k]
        la -= k
        lb -= k

    # --- Re-check trivial cases after trimming. ---
    if la == 0:
        return lb
    if lb == 0:
        return la
    if a == b:
        return 0

    # --- Make ``a`` the shorter string so the row length is minimal. ---
    if la > lb:
        a, b = b, a
        la, lb = lb, la

    # --- Two-row DP. ---
    # prev corresponds to the previous column of b (j-1); curr to column j.
    prev = list(range(la + 1))
    curr = [0] * (la + 1)

    # Cache bound method lookups / locals for the hot inner loop.
    a_local = a
    b_local = b
    for j in range(1, lb + 1):
        cb = b_local[j - 1]
        curr_j0 = j
        curr[0] = curr_j0
        prev_i_minus_1 = j - 1  # == prev[0] for this row's i=1 computation
        # i = 1 .. la
        for i in range(1, la + 1):
            # cost = 0 if a[i-1]==cb else 1
            cost = 0 if a_local[i - 1] == cb else 1
            d = prev_i_minus_1 + cost          # substitution / match
            x = prev[i] + 1                    # deletion (from a)
            if x < d:
                d = x
            x = curr[i - 1] + 1                # insertion (into a)
            if x < d:
                d = x
            curr[i] = d
            prev_i_minus_1 = prev[i]  # for next i: prev[i-1] becomes current prev[i]
        prev, curr = curr, prev

    return prev[la]
