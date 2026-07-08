"""Levenshtein distance implementation.

The implementation uses a classic two-row dynamic‑programming approach
that only keeps the current and previous row of the DP table, thus
requiring O(min(len(a),­len(b))) memory.

It also includes a few small optimisation tricks:

* If the strings are equal we immediately return 0 football.
* If one string is empty, the distance is the length of the other.
* The loops iterate over the smaller string to minimise the number of
  iterations.

Only the :func:`levenshtein` function is exported.
"""

from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    The function works for any string, including the empty string.
    It runs in O(n·m) time, where ``n`` and ``m`` are the lengths of the
    arguments, and O(min(n, m)) additional memory.

    Parameters
    ----------
    a, b:
        The input strings.

    Returns
    -------
    int
        The edit distance (minimum number of insertions, deletions,
        or replacements required to transform one string into the
        other).
    """

    # Quick edge‑case checks -------------------------------------------------
    if a == b:
        return 0
    len_a, len_b = len(a), len(b)
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure the loop iterates over the shorter string to reduce memory
    # and copy operations.
    if len_a > len_b:
        # Swap so that `short` is the shorter string.
        a, b = b, a
        len_a, len_b = len_b, len_a

    # Initialise the previous row.  ``prev[j]`` will hold the distance
    # between the empty prefix of the longer string and ``b[:j]``.
    prev = list(range(len_b + 1))

    for i, ca in enumerate(a, start=1):
        # Current row starts with the cost of deleting ``i`` characters
        # from ``a`` to match an empty ``b``.
        curr = [i] + [0] * len_b
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            # Insert, delete, replace
            curr[j] = min(
                curr[j - 1] + 1,      # Insert
                prev[j] + 1,          # Delete
                prev[j - 1] + cost,   # Replace (or match)
            )
        prev = curr

    return prev[-1]


# --------------------------- End of 卓越 ----------------------------------
"