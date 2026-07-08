#!/usr/bin/env python3
"""Compute the Levenshtein (edit) distance between two strings.

The implementation uses a classic dynamic‑programming algorithm that
keeps only two rows of the DP matrix in memory, allowing an O(mn)
time complexity and O(min(m,n)) space where `m=len(a)` and `n=len(b)`.

Early exits:
    * If the strings are identical we immediately return 0.
    * If one string is empty we immediately return the length of the
      other string.

The function is deliberately written with local variable bindings
and list pre‑allocation for speed; no external modules are required.
"""

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein distance between *a* and *b*.

    Parameters
    ----------
    a, b : str
        Input strings; may be empty.

    Returns
    -------
    int
        The edit distance.
    """

    # Quick, common‑case checks
    if a is b:
        # Same object (very common when calling with literals)
        return 0
    if a == b:
        return 0
    if not b:
        return len(a)
    if not a:
        return len(b)

    # Ensure ``b`` is the shorter string to minimise memory usage.
    if len(b) > len(a):
        a, b = b, a

    m, n = len(a), len(b)
    # Previous and current rows of the DP matrix
    prev_row = list(range(n + 1))  # Cost of converting empty `a` prefix to b[:j]
    curr_row = [0] * (n + 1)

    # Main DP loop: iterate over each character in ``a``
    for i, ca in enumerate(a, start=1):
        curr_row[0] = i  # Cost of deleting i characters from ``a``
        # Inline access to local variables for speed.
        prev_j = prev_row[0]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            # ``prev_j`` is prev_row[j-1] from previous iteration of inner loop
            insertion = prev_row[j] + 1
            deletion = curr_row[j - 1] + 1
            substitution = prev_j + cost
            curr_row[j] = min(insertion, deletion, substitution)
            prev_j = prev_row[j]
        # Swap rows for next iteration
        prev_row, curr_row = curr_row, prev_row

    # After the loop, ``prev_row`` holds the final DP results.
    return prev_row[n]

# If run as a script, allow quick manual checks.
if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        print(levenshtein(sys.argv[1], sys.argv[2]))
    else:
        print("Usage: python levenshtein.py <string1> <string2>")

"""
PY