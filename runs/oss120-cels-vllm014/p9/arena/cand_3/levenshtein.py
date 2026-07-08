# levenshtein.py
"""Utility module providing a fast Levenshtein distance implementation.

The :func:`levenshtein` function computes the edit distance between two
strings using a classic dynamic‑programming algorithm that only stores two
rows of the DP table (``O(min(m, n))`` memory).  It handles empty strings
correctly and works with any Unicode input.

The implementation is deliberately lightweight – it relies solely on the
Python standard library and strives for speed by:

* iterating over the shorter string in the inner loop, which reduces the
  number of iterations;
* using ``range`` and local variable lookups for tight loops;
* performing an early return when one of the inputs is empty.
"""

from __future__ import annotations

from typing import Iterable, List

def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    The distance is the minimum number of single‑character insertions,
    deletions, or substitutions required to transform *a* into *b*.

    Parameters
    ----------
    a, b:
        Input strings. They may be empty and may contain any Unicode
        characters.

    Returns
    -------
    int
        The edit distance.
    """
    # Fast path for trivial cases
    if a == b:
        return 0
    len_a, len_b = len(a), len(b)
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure that ``b`` is the shorter string to minimise the DP row size.
    if len_b > len_a:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # ``previous`` holds distances for the row i‑1, ``current`` for row i.
    previous: List[int] = list(range(len_b + 1))
    current: List[int] = [0] * (len_b + 1)

    # Iterate over characters of the longer string ``a``.
    for i, ca in enumerate(a, start=1):
        current[0] = i  # distance of transforming a[:i] -> '' (i deletions)
        # Inner loop over the shorter string ``b``.
        for j, cb in enumerate(b, start=1):
            # Compute cost of substitution.
            substitution_cost = 0 if ca == cb else 1
            # Minimum of deletion, insertion, substitution.
            delete = previous[j] + 1          # delete ca
            insert = current[j - 1] + 1       # insert cb
            substitute = previous[j - 1] + substitution_cost
            current[j] = min(delete, insert, substitute)
        # Swap rows for next iteration.
        previous, current = current, previous

    # After the final swap, ``previous`` holds the last computed row.
    return previous[len_b]

__all__: Iterable[str] = ["levenshtein"]
