"""Levenshtein distance implementation.

This module exposes a single function ``levenshtein(a, b)`` which returns
the edit distance between two strings ``a`` and ``b``.

The implementation uses a classic dynamic‑programming approach with a
two‑row table to keep memory usage small (O(min(len(a), len(b)))
space).  The algorithm is fast and works for all inputs, including empty
strings.

Typical usage::

    from levenshtein import levenshtein
    dist = levenshtein("kitten", "sitting")  # 3

The implementation is fully self‑contained and only depends on the
Python standard library.
"""

from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between two strings.

    Parameters
    ----------
    a, b : str
        Input strings.

    Returns
    -------
    int
        Minimum number of insertions, deletions, and substitutions required
        to transform ``a`` into ``b``.

    Notes
    -----
    * Handles empty strings.
    * Uses a two‑row dynamic programming table for O(min(len(a), len(b)))
      memory consumption.
    * Execution time is dominated by the double loop; which is the
      standard optimal solution for this problem.
    """

    # Quick path for equal strings.
    if a == b:
        return 0

    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la

    # Ensure a is the shorter string to minimise the DP row size.
    if la > lb:
        a, b = b, a
        la, lb = lb, la

    # "prev" holds the previous DP row; ``cur`` holds the current row.
    prev = list(range(la + 1))  # distance from empty prefix of a
    cur = [0] * (la + 1)

    for i in range(1, lb + 1):
        cur[0] = i  # distance from empty prefix of b
        bi = b[i - 1]
        for j in range(1, la + 1):
            cost = 0 if a[j - 1] == bi else 1
            cur[j] = min(
                prev[j] + 1,   # deletion
                cur[j - 1] + 1,  # insertion
                prev[j - 1] + cost,  # substitution
            )
        # Swap rows for next iteration (reuse lists to avoid allocation).
        prev, cur = cur, prev

    # After the loop, ``prev`` contains the final row.
    return prev[la]

# When this module is executed directly, run a small sanity test.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Levenshtein library loaded – no further output.")
