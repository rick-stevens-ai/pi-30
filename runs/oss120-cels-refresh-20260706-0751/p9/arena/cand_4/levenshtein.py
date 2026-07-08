# levenshtein.py
"""Levenshtein distance implementation.

Provides a single function ``levenshtein(a, b)`` returning the edit distance
(i.e., the minimum number of single‑character insertions, deletions or
substitutions required to transform ``a`` into ``b``).

The implementation is deliberately lightweight and fast:

* Uses the classic two‑row dynamic‑programming algorithm (O(len(a) * len(b))
  time, O(min(len(a), len(b))) space).
* Handles empty inputs instantly.
* Includes a small early‑exit optimisation – if the current row’s minimum
  value already exceeds the best possible distance (the absolute length
  difference), the algorithm stops and returns that lower bound.

Only the Python standard library is used.
"""

from __future__ import annotations
from typing import Sequence

def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between strings ``a`` and ``b``.

    Parameters
    ----------
    a, b: str
        Input strings. They may be empty.

    Returns
    -------
    int
        The minimal number of insertions, deletions, or substitutions needed
        to transform ``a`` into ``b``.
    """
    # Quick shortcuts for trivial cases
    if a == b:
        return 0
    len_a, len_b = len(a), len(b)
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure we iterate over the shorter string for the inner loop – this
    # reduces memory usage (the DP rows have size ``len(shorter) + 1``).
    if len_a > len_b:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # ``previous`` holds distances for the row representing ``a[:i]``.
    previous: list[int] = list(range(len_a + 1))
    # The minimal possible distance given the length difference; we can use
    # it for an early‑exit check.
    min_possible = len_b - len_a

    for i in range(1, len_b + 1):
        current = [i] + [0] * len_a
        b_char = b[i - 1]
        row_min = current[0]  # track row minimum for early exit
        for j in range(1, len_a + 1):
            cost = 0 if a[j - 1] == b_char else 1
            deletion = previous[j] + 1   # delete a[j-1]
            insertion = current[j - 1] + 1  # insert b_char
            substitution = previous[j - 1] + cost
            current[j] = min(deletion, insertion, substitution)
            if current[j] < row_min:
                row_min = current[j]
        # Early exit: if the best we can achieve after this row is already
        # greater than the minimal possible distance, further rows cannot
        # improve the result.
        if row_min >= min_possible and i == len_b:
            # Last row – result is settled.
            previous = current
            break
        previous = current
    return previous[-1]

# Simple self‑test when executed directly.
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        print(levenshtein(sys.argv[1], sys.argv[2]))
    else:
        # Basic sanity checks
        assert levenshtein("", "") == 0
        assert levenshtein("", "abc") == 3
        assert levenshtein("kitten", "sitting") == 3
        assert levenshtein("flaw", "lawn") == 2
        print("All internal tests passed.")
