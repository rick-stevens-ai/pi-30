"""Levenshtein edit distance with two-row DP and early exit.

Candidate #3: prefix/suffix trimming + provably-correct bound-based
early termination.  Stdlib only.

The early exit uses two facts that hold for the full-matrix cost D[i][j]
(distance between a_sub[:i] and b_sub[:j]):

  * Lower bound at row i:  D[m][n] >= min_j D[i][j] + max(0, (m-i) - n)
    because every path from (i,j) to (m,n) must take at least
    |(m-i) - (n-j)| diagonal-deficit steps, minimized over j.

  * Upper bound at row i:  D[m][n] <= D[i][n] + (m-i)
    because we can finish by deleting the remaining m-i characters of a.

Tightening the running upper bound k each row and aborting as soon as
the lower bound reaches k is exact (answer <= k and answer >= lb >= k
forces answer == k).
"""

from typing import Sequence


def levenshtein(a, b):
    # type: (Sequence, Sequence) -> int
    """Minimum single-char insertions/deletions/substitutions to turn
    ``a`` into ``b``.  Exact for all inputs (incl. empty)."""

    la = len(a)
    lb = len(b)

    # --- Empty fast paths ---------------------------------------------
    if la == 0:
        return lb
    if lb == 0:
        return la

    # Keep b as the shorter side so the DP row width is min(la, lb).
    if lb > la:
        a, b = b, a
        la, lb = lb, la

    # --- Common-prefix trimming ---------------------------------------
    # Matching leading elements cost nothing; skip them for free before
    # allocating any DP storage.
    start = 0
    while start < lb and a[start] == b[start]:
        start += 1
    if start == lb:
        # b fully matched by prefix; leftover a tail is pure deletions.
        return la - start

    # --- Common-suffix trimming ---------------------------------------
    end_a, end_b = la, lb
    while end_b > start and a[end_a - 1] == b[end_b - 1]:
        end_a -= 1
        end_b -= 1

    # Subproblem: a[start:end_a] (length m) vs b[start:end_b] (length n).
    m = end_a - start
    n = end_b - start  # m >= n

    resid_diff = m - n  # >= 0; unavoidable deletion floor for subproblem.

    # Running upper bound on the final answer.  A valid initial UB for
    # the subproblem is m: substitute all n positions then delete the
    # remaining m - n characters (cost n + (m - n) = m).
    k = m

    # --- Two-row DP ---------------------------------------------------
    prev = list(range(n + 1))  # row 0
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        ai = a[start + i - 1]
        row_min = i

        for j in range(1, n + 1):
            cost = 0 if ai == b[start + j - 1] else 1
            ins = curr[j - 1] + 1
            dele = prev[j] + 1
            sub = prev[j - 1] + cost
            v = ins if ins < dele else dele
            if sub < v:
                v = sub
            curr[j] = v
            if v < row_min:
                row_min = v

        # Tighten UB: D[m][n] <= D[i][n] + (m - i).
        ub_i = curr[n] + (m - i)
        if ub_i < k:
            k = ub_i

        # Lower bound on final answer from this row.
        lb_i = row_min + (resid_diff - i if resid_diff > i else 0)

        if lb_i >= k:
            # answer <= k and answer >= lb_i >= k  =>  answer == k.
            return k

        prev, curr = curr, prev

    return prev[n]


if __name__ == "__main__":
    import sys

    def _expect(a, b, exp):
        got = levenshtein(a, b)
        assert got == exp, f"{a!r} {b!r}: got {got} want {exp}"

    _expect("", "", 0)
    _expect("", "abc", 3)
    _expect("abc", "", 3)
    _expect("abc", "abc", 0)
    _expect("kitten", "sitting", 3)
    _expect("sitting", "kitten", 3)
    _expect("saturday", "sunday", 3)
    _expect("flaw", "lawn", 2)
    _expect("gumbo", "gambol", 2)
    _expect("book", "back", 2)
    _expect("abcd", "acbd", 2)
    _expect("x" * 50 + "abc", "x" * 50 + "abd", 1)
    _expect([1, 2, 3], [1, 2, 3], 0)
    _expect([1, 2, 3], [1, 2, 2, 3], 1)
    _expect([1, 2, 3, 4], [4, 3, 2, 1], 4)
    _expect("a" * 1000, "a" * 1000, 0)
    _expect("a" * 999 + "b", "a" * 1000, 1)
    _expect("abcdef", "abc", 3)
    print("all tests passed", file=sys.stderr)
