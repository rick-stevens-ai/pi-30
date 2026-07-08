"""Levenshtein distance implementation.

Provides a single function ``levenshtein(a, b)`` returning the edit distance
between two strings (or any sequence of hashable elements).  The implementation
is **O(min(len(a), len(b)))** memory and **O(len(a) * len(b))** time, using the
classic two‑row dynamic programming algorithm with a simple early‑exit
optimisation: if the minimum possible distance for the current row already
exceeds a previously computed bound we stop processing.

Only the Python standard library is used.
"""

from __future__ import annotations
from typing import Sequence

__all__ = ["levenshtein"]


def _validate_input(a: Sequence, b: Sequence) -> None:
    """Validate that *a* and *b* are sequences.

    The function deliberately accepts any ``Sequence`` (including ``str``)
    because the algorithm works on generic hashable elements.  A ``TypeError``
    is raised for ``None`` or objects that do not implement ``__len__``.
    """
    if a is None or b is None:
        raise TypeError("Input strings must not be None")
    # ``len`` will raise TypeError if the object is not sized – we let that
    # propagate as a clear error message.
    _ = len(a)  # noqa: B018
    _ = len(b)  # noqa: B018


def levenshtein(a: Sequence, b: Sequence) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    The distance is the minimum number of single‑character insertions,
    deletions or substitutions required to change *a* into *b*.

    Features
    --------
    * Works with any ``Sequence`` (strings, lists, tuples, etc.).
    * Handles empty inputs correctly.
    * Uses only two rows of the DP table (O(min(n, m)) memory).
    * Includes an early‑exit optimisation: if during processing the smallest
      value in the current row exceeds the best possible distance already found
      (which for a full DP table is the final result), the loop terminates early.

    Parameters
    ----------
    a, b:
        Sequences to compare.

    Returns
    -------
    int
        The Levenshtein distance.
    """
    _validate_input(a, b)

    # Ensure ``a`` is the shorter sequence to minimise memory usage.
    if len(a) > len(b):
        a, b = b, a
    n, m = len(a), len(b)

    # Quick return for empty inputs.
    if n == 0:
        return m
    if m == 0:
        return n

    # ``previous`` holds the DP values for the row that corresponds to
    # ``a[:i]``; ``current`` will be filled for ``a[:i+1]``.
    previous = list(range(n + 1))
    current = [0] * (n + 1)

    # The best distance we have seen so far; initialise with the maximum
    # possible distance (i.e., converting the whole of ``b`` to ``a``).
    best = m

    for j in range(1, m + 1):
        # First column always equals the number of deletions needed to match
        # an empty ``b`` prefix.
        current[0] = j
        # Track the minimum value in this row for early exit.
        row_min = current[0]
        bj = b[j - 1]
        for i in range(1, n + 1):
            cost = 0 if a[i - 1] == bj else 1
            # DP recurrence: minimum of deletion, insertion, substitution.
            deletion = previous[i] + 1
            insertion = current[i - 1] + 1
            substitution = previous[i - 1] + cost
            cur = deletion if deletion < insertion else insertion
            cur = cur if cur < substitution else substitution
            current[i] = cur
            if cur < row_min:
                row_min = cur
        # Early exit: if the smallest entry in the current row already exceeds
        # the best possible distance (which cannot be smaller than ``row_min``),
        # further rows will only increase the distance.
        if row_min >= best:
            # The distance cannot improve beyond ``row_min``; we can break.
            best = row_min
            break
        # Swap rows for next iteration.
        previous, current = current, previous
        # Update best with the last element of the processed row, which is the
        # distance for the prefix ``b[:j]`` against the full ``a``.
        best = previous[n]

    return best

# ---------------------------------------------------------------------------
# Simple sanity check when the module is executed directly.
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python levenshtein.py <string1> <string2>")
        sys.exit(1)
    s1, s2 = sys.argv[1], sys.argv[2]
    print(levenshtein(s1, s2))
