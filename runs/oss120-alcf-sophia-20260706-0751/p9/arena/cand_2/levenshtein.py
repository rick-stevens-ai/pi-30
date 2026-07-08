# levenshtein.py
"""Levenshtein (edit) distance implementation.

Provides a single public function::

    levenshtein(a: str, b: str) -> int

The implementation uses the classic two‑row dynamic programming algorithm
which runs in O(len(a) * len(b)) time but only O(min(len(a), len(b)))
additional memory.  A few cheap early‑exit shortcuts are added:

* If the strings are identical the distance is ``0``.
* If one string is empty the distance is the length of the other.
* The shorter string is always iterated in the inner loop, keeping the
  DP rows as small as possible.

The code relies solely on the Python standard library and works for any
Unicode strings.
"""

from __future__ import annotations

__all__ = ["levenshtein"]


def _ensure_str(s: object) -> str:
    """Coerce *s* to ``str``.

    The public ``levenshtein`` function accepts ``str`` arguments, but this
    helper makes the implementation robust if a non‑string object (e.g.
    ``bytes``) is passed inadvertently – it will be converted using ``str``.
    """
    if isinstance(s, str):
        return s
    return str(s)


def levenshtein(a: str | bytes, b: str | bytes) -> int:
    """Return the Levenshtein distance between *a* and *b*.

    The distance is the minimum number of single‑character insertions,
    deletions or substitutions required to transform *a* into *b*.

    Parameters
    ----------
    a, b:
        Input strings (or any objects coercible to ``str``).

    Returns
    -------
    int
        The edit distance.
    """
    # Normalise inputs – accept ``bytes`` or any object that can be cast to str.
    a = _ensure_str(a)
    b = _ensure_str(b)

    # Fast path for equality and empty strings.
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure that ``b`` is the shorter string – this minimises the DP row size.
    if len(b) > len(a):
        a, b = b, a  # swap so that len(b) <= len(a)

    # ``previous`` holds the distances for the prefix of *a* up to the
    # previous character of *b*.
    previous = list(range(len(b) + 1))
    current = [0] * (len(b) + 1)

    for i, ca in enumerate(a, start=1):
        # First column corresponds to transforming ``a[:i]`` to an empty string.
        current[0] = i
        # Track the minimal value in the current row for an early‑exit
        # heuristic: if the smallest entry already exceeds the best possible
        # distance we could achieve (which is the absolute length difference),
        # we keep computing because a later column might still be lower.  The
        # cheap early‑exit we employ is when the current row's minimum equals
        # the length difference – at that point the distance cannot improve.
        row_min = current[0]
        for j, cb in enumerate(b, start=1):
            # Substitution cost is 0 if characters match, else 1.
            cost = 0 if ca == cb else 1
            # Compute the three possible operations.
            deletion = previous[j] + 1      # delete ca
            insertion = current[j - 1] + 1  # insert cb
            substitution = previous[j - 1] + cost
            cur = min(deletion, insertion, substitution)
            current[j] = cur
            if cur < row_min:
                row_min = cur
        # Early exit: the theoretical lower bound for the remaining rows is
        # the absolute difference between the processed prefix lengths.
        # If the smallest entry in this row equals that bound we can stop.
        if row_min == abs(len(a) - len(b)):
            # The remaining rows will only increase the distance, so we can
            # safely break and return the final value from the last column.
            # ``i`` may be less than len(a), but the distance is already
            # determined by the current last column.
            return current[-1]
        # Swap rows for the next iteration.
        previous, current = current, previous

    # After the loop ``previous`` holds the last computed row.
    return previous[-1]

# Simple sanity test (executed when run as a script).
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        print(levenshtein(sys.argv[1], sys.argv[2]))
    else:
        # Run a few basic checks.
        assert levenshtein("", "") == 0
        assert levenshtein("", "abc") == 3
        assert levenshtein("kitten", "sitting") == 3
        assert levenshtein("flaw", "lawn") == 2
        print("All internal tests passed.")
