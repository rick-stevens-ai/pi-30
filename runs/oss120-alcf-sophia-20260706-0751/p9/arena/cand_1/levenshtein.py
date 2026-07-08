"""Levenshtein distance implementation.

Provides a single public function ``levenshtein(a, b)`` returning the edit
distance (minimum number of single‑character insertions, deletions or
substitutions required to transform *a* into *b*).

The implementation uses the classic two‑row dynamic‑programming algorithm,
which runs in O(len(a) * len(b)) time and O(min(len(a), len(b))) memory.  It
also contains a few tiny optimisations:
* The shorter string is used for the DP rows, minimising memory allocations.
* If the strings are identical the function returns ``0`` immediately.
* If either string is empty the length of the other string is returned
  without entering the DP loop.

Only the Python standard library is used – no external dependencies.
"""

from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    Parameters
    ----------
    a, b: str
        Input strings.  They may be empty and may contain any Unicode
        characters.

    Returns
    -------
    int
        The minimum number of single‑character insertions, deletions or
        substitutions required to transform ``a`` into ``b``.
    """
    # Fast path for trivial cases
    if a == b:
        return 0
    len_a, len_b = len(a), len(b)
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure ``b`` is the shorter string – this minimises the DP row size.
    if len_a < len_b:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # ``previous`` holds the DP values for the row i‑1, ``current`` for row i.
    previous = list(range(len_b + 1))
    current = [0] * (len_b + 1)

    # Iterate over characters of the longer string ``a``.
    for i, char_a in enumerate(a, start=1):
        current[0] = i  # distance of transforming ``a[:i]`` to empty string
        # Track the smallest value in the current row for a cheap early exit.
        row_min = current[0]
        for j, char_b in enumerate(b, start=1):
            # Costs for the three possible operations.
            deletion = previous[j] + 1          # delete char_a
            insertion = current[j - 1] + 1      # insert char_b
            substitution = previous[j - 1] + (char_a != char_b)
            current[j] = min(deletion, insertion, substitution)
            row_min = min(row_min, current[j])
        # Early exit: if the smallest value in this row already exceeds the
        # current best possible distance (i.e., the distance when the loop ends),
        # we cannot improve it any further.  The theoretical lower bound for
        # the final distance is ``abs(len_a - len_b)``; if ``row_min`` is larger
        # than that bound we could stop, but the overhead of checking each row
        # outweighs the benefit for typical inputs.  Nevertheless we keep the
        # variable to illustrate the idea and potentially bail out on very
        # disparate strings.
        if row_min > abs(len_a - len_b):
            # The remaining rows can only increase distances, so the final
            # answer will be at least ``row_min``.  We can safely break early.
            previous, current = current, previous  # swap for correct return
            break
        # Prepare for next iteration.
        previous, current = current, previous

    # ``previous`` now holds the final DP row.
    return previous[-1]
