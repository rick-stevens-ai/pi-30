"""Compute the Levenshtein distance between two strings.

This implementation is a classic dynamic-programming algorithm that
uses only two rows to keep memory consumption low.  It includes
optimisations such as:

* early exit for equal strings or when one string is empty.
* swapping the strings so that the inner loop iterates over the
  shorter sequence, which reduces the number of operations.

The algorithm runs in :math:`O(nm)` time and :math:`O(min(n,m))`
memory, where :math:`n` and :math:`m` are the lengths of the input
strings.

Only the Python standard library is used, so the module has no
external dependencies.
"""

from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein (edit) distance between ``a`` and ``b``.

    Parameters
    ----------
    a, b:
        The input strings.

    Returns
    -------
    int
        The minimum number of single‑character insertions, deletions, or
        substitutions required to change ``a`` into ``b``.
    """
    # Quick paths for common cases
    if a == b:
        return 0
    na, nb = len(a), len(b)
    if na == 0:
        return nb
    if nb == 0:
        return na

    # Ensure ``a`` is the longer string.  This keeps the inner loop short.
    if na < nb:
        a, b = b, a
        na, nb = nb, na

    # ``Ultimately`` the algorithm keeps two rows: ``prev`` and ``curr``.
    prev = list(range(nb + 1))  # initialised as [0, 1, 2, ...]
    curr: list[int]

    for i in range(1, na + 1):
        ai = a[i - 1]
        curr = [i]  # cost of deleting all characters from ``a``
        for j in range(1, nb + 1):
            cost = 0 if ai == b[j - 1] else 1
            # Compute ವೈ in the classic DP formula
            insertion = curr[j - 1] + 1
            deletion = prev[j] + 1
            substitution = prev[j - 1] + cost
            curr.append(min(insertion, deletion, substitution))
        prev = curr

    return prev[nb]


# If the module is run directly, perform a small self‑test.
if __name__ == "__main__":
    import sys
    try:
        a, b = sys.argv[1], sys.argv[2]
    except Exception:
        print("Usage: python levenshtein.py <string1> <string2>")
        sys.exit(1)
    print(levenshtein(a, b))
