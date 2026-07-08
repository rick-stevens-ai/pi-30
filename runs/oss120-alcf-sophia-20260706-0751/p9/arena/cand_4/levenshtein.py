"""Levenshtein distance implementation.

Provides a single function ``levenshtein(a, b)`` that computes the edit
distance (minimum number of single‑character insertions, deletions or
substitutions) between two strings ``a`` and ``b``.

The implementation uses a memory‑efficient two‑row dynamic programming
algorithm (O(min(len(a), len(b))) space) and a few cheap early‑exit
optimisations:

* If either string is empty we can return the length of the other one.
* If the strings are identical we return ``0`` immediately.
* The shorter string is used for the inner loop to minimise the number of
  iterations.

Only the Python standard library is used, making the module portable and
fast enough for typical use‑cases (e.g. spell‑checking, fuzzy matching).
"""

from __future__ import annotations

from typing import List

__all__: List[str] = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between ``a`` and ``b``.

    Parameters
    ----------
    a, b:
        The strings to compare. They may be empty and can contain any
        Unicode characters.

    Returns
    -------
    int
        The minimum number of single‑character insertions, deletions, or
        substitutions required to transform ``a`` into ``b``.

    Notes
    -----
    The implementation runs in O(len(a) * len(b)) time but only stores two
    rows of the DP matrix, giving O(min(len(a), len(b))) additional memory.
    ``a`` is swapped with ``b`` if ``b`` is shorter so that the inner loop
    iterates over the smaller string.
    """
    # Fast path for trivial cases.
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la

    # Ensure that ``b`` is the shorter string – this reduces the inner loop
    # length and therefore the memory footprint.
    if lb > la:
        a, b = b, a
        la, lb = lb, la

    # ``previous`` holds the DP values for the row i-1, ``current`` for row i.
    previous = list(range(lb + 1))
    current = [0] * (lb + 1)

    for i in range(1, la + 1):
        # First column corresponds to transforming a[:i] into an empty string.
        current[0] = i
        ai = a[i - 1]
        # Compute the rest of the row.
        for j in range(1, lb + 1):
            cost = 0 if ai == b[j - 1] else 1
            # Minimum of deletion, insertion, substitution.
            deletion = previous[j] + 1
            insertion = current[j - 1] + 1
            substitution = previous[j - 1] + cost
            current[j] = min(deletion, insertion, substitution)
        # Swap rows for next iteration.
        previous, current = current, previous

    # After the final swap, ``previous`` holds the last computed row.
    return previous[lb]
