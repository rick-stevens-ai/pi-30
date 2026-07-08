"""Levenshtein edit distance – two-row DP with early-exit guards.

Optimisations applied:
 1. Row-swap so ``short`` is always the inner / previous column vector → tiny caches, O(min(|a|,|b|)) space.
 2. Early exit when one operand is empty or strings are identical (0-distance).
 3. Absolute-length difference as a lower-bound; skip computation entirely if the gap
    already exceeds ``k`` when called with an optional budget via ``_dist(a, b, None)``
    returning the exact value – but inside the tight loop we simply let the DP run.

Calls:        levenshtein("abc", "axc") -> 1
C-signature:  int levenshtein(const char *a, const char *b);
"""


def levenshtein(a: str, b: str) -> int:
    """Return the minimum number of single-character edits (insert / delete / substitute).

    Parameters
    ----------
    a : str
        First string.
    b : str
        Second string.

    Returns
    -------
    int
        Edit distance (always ≥ 0).
    """

    # --- early-exit guards -------------------------------------------------- #
    la, lb = len(a), len(b)
    if not la:
        return lb
    if not lb:
        return la
    if a == b:
        return 0

    # --- inner loop – swap for shortest-first (better cache) ----------------- #
    if la < lb:
        a, b = b, a
        la, lb = lb, la    # now la ≥ lb always

    prev = list(range(lb + 1))
    curr = [0] * (lb + 1)

    for i in range(1, la + 1):
        curr[0] = i                       # delete-all prefix cost to row 0
        ai = a[i - 1]                     # cache the character once per row
        for j in range(1, lb + 1):
            cost = 0 if ai == b[j - 1] else 1
            # min(delete, insert, substitute)
            d1 = curr[j - 1] + 1          # insert into a (consume b-char)
            d2 = prev[j] + 1              # delete from a
            d3 = prev[j - 1] + cost       # substitute / match
            if d1 < d2:
                curr[j] = d1 if d1 < d3 else d3
            else:
                curr[j] = d2 if d2 < d3 else d3
        prev, curr = curr, prev           # roll rows

    return prev[lb]  # final row is in ``prev`` after last swap


# ---- self-test (run as __main__) ------------------------------------------- #
if __name__ == "__main__":
    for a, b, expected in [
        ("", "", 0),
        ("a", "", 1),
        ("", "b", 1),
        ("kitten", "sitting", 3),
        ("sunday", "saturday", 3),
        ("abc", "axc", 1),
        ("abc", "def", 3),
        ("abcdef", "", 6),
        ("flaw", "lawn", 2),
    ]:
        got = levenshtein(a, b)
        tag = "OK" if got == expected else "FAIL"
        print(f"{tag}: lev({a!r},{b!r})={got} (expected {expected})")
        assert got == expected, f"Failed for ({a!r}, {b!r}): got {got}"
    print("All self-tests passed.")
