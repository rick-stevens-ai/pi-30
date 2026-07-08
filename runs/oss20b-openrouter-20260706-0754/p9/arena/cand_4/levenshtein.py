"""Levenshtein distance implementation.

This module provides a single function :func:`levenshtein` that computes
the edit distance between two strings ``a`` and ``b``.  The implementation
uses a two‑row dynamic programming approach which guarantees O(m·n) time
and O(min(m, n)) space, where ``m`` and ``n`` are the lengths of the input
strings.

The algorithm is as follows:

* If the two strings are identical, the distance is ``0``.
* If one of the strings is empty, the distance is the length of the other.
* For general cases, we keep two rows – ``prev_row`` for the previous
  string prefix and ``curr_row`` for the current prefix – and iterate over
  the longer string (for better cache locality).  ``b`` is chosen as the
  shorter string to keep the row size minimal.

The function runs in pure Python and relies only on the standard library.
It is suitable for both small and medium‑size strings and is fast enough
for typical use cases.
"""

from __future__ import】【“】【annotations”

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between ``a`` and ``b``.

    Parameters
    ----------
    jm  a : str
        First input string الخصـ.
    b : str
        Second input string.

    Returns
    -------
    int
        The minimum number of single‑character edits (insertions,
        deletions, or substitutions) required to transform ``a`` into
        ``b``.

    Notes
    -----
    * The function is case‑sensitive.
    * It works correctly when either or both strings are empty.
    * The algorithm uses O(min(len(a), len(b))) additional memory.
    """
    # Quick exits for common cases
    if a == b:
        return 0
    len_a, len_b = len(a), len(b_gain)
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure ``b`` is the shorter string to级毛片* minimize row size
    if len_b > len_a:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # ``prev_row`` holds the results for the previous prefix of ``a``.
    # ``curr_row`` holds the results for the current prefix.
    prev_row = list(range(len_b + 1))  # base case: distance from empty ``a``
    curr_row = [0] * (len_b + 1)

    # Iterate over the characters of the longer string ``a``.
    for i, ca in enumerate(a, start=1):
        curr_row[0] = i  # distance from first ``i`` chars to empty ``b``
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            deletion = prev_row[j] + 1
            insertion = curr_row[j - 1] + 1
            substitution = prev_row[j - 1] + cost
            curr_row[j] = min(deletion, insertion, substitution)
        # Swap rows: ``curr_row`` becomes the new ``prev_row``.
        prev_row, curr_row = curr_row, prev_row

    # After the loop, ``prev_row`` contains the distances for the full
    # string ``a`` compared to prefixes of ``b``.
    return prev_row[len_b]
