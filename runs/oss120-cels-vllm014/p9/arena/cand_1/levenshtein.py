"""Levenshtein distance implementation.

Provides a single function ``levenshtein(a, b)`` returning the edit distance
between two strings ``a`` and ``b``.

The implementation uses the classic two‑row dynamic programming algorithm
which runs in O(len(a) * len(b)) time and O(min(len(a), len(b))) space.  It also
includes a few cheap early‑exit checks to speed up common cases:

* If the strings are identical, return ``0``.
* If either string is empty, return the length of the other.
* The shorter string is used for the DP rows, minimising memory usage.

Only the Python standard library is used.
"""

from __future__ import annotations

from typing import Iterable

__all__: Iterable[str] = ("levenshtein",)


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between ``a`` and ``b``.

    The distance is the minimum number of single‑character insertions,
    deletions, or substitutions required to transform ``a`` into ``b``.

    Parameters
    ----------
    a, b:
        Input strings. They may be empty.

    Returns
    -------
    int
        The edit distance.
    """
    # Fast path for identical strings.
    if a == b:
        return 0

    # Ensure ``a`` is the shorter string to minimise allocation.
    if len(a) > len(b):
        a, b = b, a

    len_a, len_b = len(a), len(b)
    # If the shorter string is empty, distance equals length of the other.
    if len_a == 0:
        return len_b

    # Initialise two rows for DP. ``prev`` holds the previous row, ``curr`` the
    # current one.  The first row corresponds to transforming the empty prefix
    # of ``a`` into prefixes of ``b`` – i.e. simple insertions.
    prev = list(range(len_b + 1))
    curr = [0] * (len_b + 1)

    # Iterate over characters of ``a``.
    for i, ca in enumerate(a, start=1):
        # First column: transforming ``a[:i]`` into empty ``b`` requires i deletions.
        curr[0] = i
        # Track the minimum value in the current row for early exit.
        row_min = curr[0]
        for j, cb in enumerate(b, start=1):
            # Compute costs for the three possible operations.
            deletion = prev[j] + 1      # delete ca
            insertion = curr[j - 1] + 1  # insert cb
            substitution = prev[j - 1] + (ca != cb)
            cost = min(deletion, insertion, substitution)
            curr[j] = cost
            if cost < row_min:
                row_min = cost
        # Early exit: if the smallest entry in the current row exceeds the
        # theoretical lower bound (the absolute length difference), the final
        # distance cannot be smaller than that bound, but we cannot stop yet.
        # However, if row_min is already larger than the current best possible
        # distance (which is |len_a - len_b|), we could break.  Here we just keep
        # the simple optimisation of swapping rows.
        prev, curr = curr, prev
    # After the final swap, ``prev`` holds the last computed row.
    return prev[len_b]
