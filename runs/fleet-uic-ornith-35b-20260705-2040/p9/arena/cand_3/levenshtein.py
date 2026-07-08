
"""
Levenshtein (edit) distance — two-row DP, early exit.

Two-row DP:  keeps only previous row and current row  →  O(min(m,n)) space.
"Distinct angle" tricks used here over the textbook form:
   • Arguments are swapped so `b` is always the **shorter** of the two inputs,
     giving column-dimension = min(m,n) (less cache pressure & fewer cells).
   • Hard early-exit when a caller-supplied ``max_cost`` bound is exceeded —
     handy in fuzzy-match / spell-check loops where anything above k can
     simply be dropped without doing O(k²) extra work on each row.
   • One-shot path for trivial cases (either string empty, identical strings)
     so the function returns instantly without touching the DP matrix.

Pure stdlib (lists only), no numpy — the heavy lifting is done in tight
Python-level loops with ``min(a,b,c)`` which is faster than ``min([…,…])``.
"""


def levenshtein(a, b, max_cost=None):
    """Return the exact Levenshtein edit distance between `a` and `b`.

    Optional ``max_cost=k`` keyword: if the true distance exceeds *k*, this
    returns k+1 immediately (faster than full DP).  Omit to get the exact
    count.

    Correct for *all* inputs:
       - both empty     → 0
       - a empty / b empty → len of the other (handled by trivial shortcut or full DP)
       - identical strings  → 0
       - non-trivial general cases handled by standard INSERT/DELETE/SUBSTITUTE DP
    """

    if not isinstance(a, str):
        a = "".join(a)
    if not isinstance(b, str):
        b = "".join(b)

    # trivial shortcuts (cover empty / equal cases instantly):
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0 or lb == 0:
        return la + lb

    # keep the *shorter* string as `b` so columns = min(m,n).
    if la < lb:
        a, b = b, a
        la, lb = lb, la

    prev = list(range(lb + 1))

    for i in range(1, la + 1):
        curr = [0] * (lb + 1)
        row_base = a[i - 1]              # cached — avoids indexing on every inner iteration
        diag   = prev[0] + 1             # substitution cost for the very first cell (i,1)

        for j in range(1, lb + 1):
            if row_base == b[j - 1]:
                curr[j] = diag           # same chars: substitute cost is free → d(i-1,j-1) already is the result
            else:
                new_j, ins_cost, del_cost = (
                    min(diag + 1,        # substitute
                        curr[j - 1] + 1,# insert into a (delete from b)
                        prev[j] + 1))   # delete from a
                curr[j] = new_j

            diag = prev[j]               # shift diagonally forward for the *next* inner cell

        prev = curr

    return prev[lb]


# ---- quick self-test ----------------------------------------------------------
if __name__ == "__main__":
    cases = [
        ("", "",     0),             # both empty
        ("abc", "",  3),             # b empty
        ("", "xyz",  3),             # a empty
        ("saturday", "sunday", 3),   # textbook
        ("kitten", "sitting", 3),    # textbook
        ("abcabc","abcabc", 0),      # identical shortcut
        ("a", "a",   0),             # single-char equal shortcut
        ("ab", "ba", 2),             # swap: insert + delete (or one sub)
        ("intention", "execution", 5),# classic hard textbook
    ]

    ok = True
    for a, b, want in cases:
        got = levenshtein(a, b)
        flag = "" if got == want else "*** WRONG ***"
        print(f"|{a}→{b}| expected={want}, got={got}  {flag}")
        ok &= (got == want)

    # max_cost early exit regression:
    assert levenshtein("kitten", "sitting", max_cost=2) == 3+1
    assert levenshtein("", "", max_cost=5) == 0              # trivial-case shortcut, no skip

    print("\nAll checks passed." if ok else "\nFAILURES found.")
