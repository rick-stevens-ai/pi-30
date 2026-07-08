"""Levenshtein distance implementation.

Provides a single function ``levenshtein(a, b)`` that returns the edit distance
between two strings (or any sequence of hashable items). The implementation uses
a two‑row dynamic programming algorithm, runs in O(len(a) * len(b)) time and
O(min(len(a), len(b))) space, and includes a simple early‑exit optimisation
that stops computation if the current minimum distance already exceeds a bound
(e.g., when one of the inputs is empty).

Only the Python standard library is used.
"""

from __future__ import annotations

from typing import Sequence


def _ensure_sequence(x: str | Sequence) -> Sequence:
    """Return ``x`` as a sequence.

    ``levenshtein`` accepts either a string or any other sequence (list, tuple,
    etc.). Strings are already sequences of characters, so we simply return the
    value. The helper exists for type‑checking clarity.
    """
    return x  # type: ignore[return-value]


def levenshtein(a: str | Sequence, b: str | Sequence) -> int:
    """Return the Levenshtein edit distance between ``a`` and ``b``.

    The distance is the minimum number of single‑character insertions,
    deletions, or substitutions required to transform ``a`` into ``b``.

    The algorithm works with any sequence type, not just strings, and gracefully
    handles empty inputs.
    """
    # Convert to sequences for uniform handling.
    a_seq = _ensure_sequence(a)
    b_seq = _ensure_sequence(b)

    # Ensure ``a_seq`` is the shorter sequence to minimise memory usage.
    if len(a_seq) > len(b_seq):
        a_seq, b_seq = b_seq, a_seq

    n, m = len(a_seq), len(b_seq)
    if n == 0:
        return m
    if m == 0:
        return n

    # ``previous`` holds the DP values for the row ``i-1`` and ``current`` for row ``i``.
    previous = list(range(m + 1))
    current = [0] * (m + 1)

    for i in range(1, n + 1):
        current[0] = i
        ai = a_seq[i - 1]
        # Track the smallest value in this row for a potential early exit.
        row_min = current[0]
        for j in range(1, m + 1):
            cost = 0 if ai == b_seq[j - 1] else 1
            deletion = previous[j] + 1
            insertion = current[j - 1] + 1
            substitution = previous[j - 1] + cost
            current[j] = min(deletion, insertion, substitution)
            if current[j] < row_min:
                row_min = current[j]
        # Early exit: if the smallest value in the row already exceeds the
        # maximum possible distance (i.e., the length of the longer string),
        # further computation cannot improve the result. This case is rare but
        # cheap to check.
        if row_min >= max(n, m):
            # The remaining rows would only increase the distance.
            return max(n, m)
        # Swap rows for the next iteration.
        previous, current = current, previous

    # ``previous`` now holds the last computed row.
    return previous[m]


__all__ = ["levenshtein"]
