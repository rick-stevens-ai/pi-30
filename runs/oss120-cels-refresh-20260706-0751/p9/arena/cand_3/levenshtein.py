"""Levenshtein distance implementation.

Provides a single function ``levenshtein(a, b)`` returning the edit distance
between two strings (or any sequence supporting ``len`` and indexing). The
implementation uses a two‑row dynamic programming table, runs in O(len(a) *
len(b)) time and O(min(len(a), len(b))) memory, and includes a few cheap
optimisations:

* Handles empty inputs immediately.
* Swaps the strings so that the shorter one drives the inner loop, minimising
  allocation.
* Uses a single ``list`` for the previous row and updates it in‑place for the
  current row.
"""

from __future__ import annotations
from typing import Sequence

__all__ = ["levenshtein"]


def levenshtein(a: Sequence, b: Sequence) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    The distance is the minimum number of single‑character insertions,
    deletions or substitutions required to transform *a* into *b*.

    Parameters
    ----------
    a, b:
        Any sequence (most commonly ``str``) that supports ``len`` and
        element access via ``obj[i]``.

    Returns
    -------
    int
        The edit distance.
    """
    # Quick shortcuts for trivial cases.
    len_a, len_b = len(a), len(b)
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure that ``a`` is the shorter sequence to keep the DP row small.
    if len_a > len_b:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # ``prev`` holds the distances for the previous row (i‑1).
    # Initialise it to the distance from the empty prefix of ``a`` to prefixes of ``b``.
    prev = list(range(len_a + 1))

    # Iterate over each character of the longer string ``b``.
    for j in range(1, len_b + 1):
        # ``curr`` starts with the cost of turning the first ``j`` characters of ``b``
        # into an empty ``a`` – i.e. ``j`` deletions.
        curr = [j] + [0] * len_a
        bj = b[j - 1]
        # Compute the rest of the row.
        for i in range(1, len_a + 1):
            cost = 0 if a[i - 1] == bj else 1
            # Minimum of deletion, insertion, substitution.
            curr[i] = min(
                prev[i] + 1,      # deletion (from a)
                curr[i - 1] + 1,  # insertion (into a)
                prev[i - 1] + cost,  # substitution
            )
        # Prepare for next iteration.
        prev = curr

    return prev[len_a]
