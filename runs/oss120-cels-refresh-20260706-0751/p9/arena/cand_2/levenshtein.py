"""levenshtein.py

Provides a fast, pure‑Python implementation of the Levenshtein edit distance.
The implementation uses a classic two‑row dynamic‑programming algorithm and
includes a few tiny optimisations (swap to ensure the shorter string drives the
inner loop, early return for identical or empty inputs).  It relies only on the
standard library and works for any hashable sequence, but the primary use‑case
is plain strings.

Example
-------
>>> from levenshtein import levenshtein
>>> levenshtein('kitten', 'sitting')
3
"""

from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    The distance is the minimum number of single‑character insertions,
    deletions or substitutions required to change one string into the other.

    This implementation runs in O(len(a) * len(b)) time but only O(min(len(a),
    len(b))) additional memory by keeping just two rows of the DP matrix.

    Edge cases:
    * If the strings are equal the distance is ``0``.
    * If either string is empty the distance is the length of the other string.
    """
    # Fast path for trivial cases
    if a == b:
        return 0
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n

    # Ensure that "b" is the shorter string to minimise the inner loop.
    # This keeps the memory usage proportional to the shorter length.
    if n < m:
        a, b = b, a
        n, m = m, n

    # ``previous`` holds the DP values for the row i‑1, ``current`` the row i.
    previous = list(range(m + 1))
    for i, ca in enumerate(a, start=1):
        # First column is always the cost of deleting i characters from ``a``.
        current = [i] + [0] * m
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            # Minimum of deletion, insertion, substitution.
            current[j] = min(
                previous[j] + 1,      # deletion (from ``a``)
                current[j - 1] + 1,   # insertion (into ``a``)
                previous[j - 1] + cost,  # substitution
            )
        previous = current
    return previous[m]
