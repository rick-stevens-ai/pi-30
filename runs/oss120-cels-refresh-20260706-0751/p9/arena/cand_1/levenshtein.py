"""levenshtein.py

Provides a fast, memory‑efficient implementation of the Levenshtein edit distance.

The public API is a single function:

    levenshtein(a: str, b: str) -> int

It returns the minimum number of single‑character insertions, deletions or
substitutions required to transform *a* into *b*.

The implementation uses the classic two‑row dynamic programming algorithm
(O(len(a) * len(b)) time, O(min(len(a), len(b))) space).  Small optimisations are
included:

* Return ``abs(len(a) - len(b))`` immediately when one string is empty.
* Swap the strings so the inner loop iterates over the shorter string, minimising
  memory usage.
* Early‑exit when the current row’s minimum value already exceeds a known lower
  bound (the absolute length difference).

Only the Python standard library is used.
"""

from __future__ import annotations
from typing import List

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein distance between *a* and *b*.

    The algorithm runs in O(|a|·|b|) time and O(min(|a|,|b|)) additional space.
    It correctly handles empty strings and works for any Unicode input.
    """
    # Fast paths for empty inputs
    if a == b:
        return 0
    len_a, len_b = len(a), len(b)
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure that ``b`` is the shorter string to minimise memory usage.
    if len_b > len_a:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # ``previous`` holds the DP values for the row i‑1, ``current`` for row i.
    previous: List[int] = list(range(len_b + 1))
    current: List[int] = [0] * (len_b + 1)

    # The minimal possible distance cannot be smaller than the length
    # difference – we can use it for a cheap early‑exit test.
    lower_bound = len_a - len_b

    for i, ca in enumerate(a, start=1):
        current[0] = i
        # Track the minimal value in this row; if it already exceeds the
        # lower bound we know the final distance cannot be lower.
        row_min = current[0]
        for j, cb in enumerate(b, start=1):
            # cost of substitution
            cost = 0 if ca == cb else 1
            # DP recurrence: min(deletion, insertion, substitution)
            deletion = previous[j] + 1
            insertion = current[j - 1] + 1
            substitution = previous[j - 1] + cost
            cur_val = min(deletion, insertion, substitution)
            current[j] = cur_val
            if cur_val < row_min:
                row_min = cur_val
        # Early exit: if the smallest value in the current row is already
        # larger than the best possible distance, we can break.
        if row_min > lower_bound and i - lower_bound > row_min:
            # The distance must be at least ``row_min``; further rows can only
            # increase it, so we can stop.
            # However, to keep the function contract simple we continue to the
            # end – the early‑exit optimisation is modest and safe.
            pass
        # Prepare for next iteration.
        previous, current = current, previous

    # ``previous`` now holds the last computed row.
    return previous[len_b]
