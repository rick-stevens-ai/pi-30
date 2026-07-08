"""Levenshtein edit distance (two-row DP, early exit for empty inputs).

Provides:
    levenshtein(a: str|bytes, b: str|bytes) -> int

Only standard library is used; works with any hashable characters by converting to
string representation if non-string iterables are supplied.
"""

def levenshtein(a, b):
    # Normalize inputs – accept any object that can be turned into a string.
    if not isinstance(a, str):
        a = ''.join(map(str, a))
    if not isinstance(b, str):
        b = ''.join(map(str, b))

    m, n = len(a), len(b)

    # Quick returns for empty inputs (early exit)
    if m == 0:
        return n
    if n == 0:
        return m

    # Ensure the shorter string is `b` to minimise memory usage.
    if m < n:
        a, b = b, a
        m, n = n, m

    # previous_row holds distances for the previous prefix of `a`
    previous_row = list(range(n + 1))

    for i in range(1, m + 1):
        current_row = [i] + [0] * n
        ai = a[i - 1]

        for j in range(1, n + 1):
            cost = 0 if ai == b[j - 1] else 1
            deletion = previous_row[j] + 1          # delete ai
            insertion = current_row[j - 1] + 1      # insert bj
            substitution = previous_row[j - 1] + cost
            current_row[j] = min(deletion, insertion, substitution)

        previous_row = current_row

    return previous_row[n]