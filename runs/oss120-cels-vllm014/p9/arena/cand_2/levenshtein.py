"""Levenshtein distance implementation.

Provides a single public function :func:`levenshtein` that computes the edit
distance between two strings using the classic dynamic‑programming algorithm
with a two‑row optimisation.  The implementation is pure Python, uses only the
standard library and is deliberately written for speed while still being easy
to read.

The algorithm works in O(min(n, m)) memory where *n* and *m* are the lengths of
the input strings.  It also includes a few cheap early‑exit shortcuts:

* If the strings are identical the distance is ``0``.
* If either string is empty the distance is the length of the other string.
* The shorter string is used for the inner loop to minimise the amount of work.

The function accepts any objects that support the ``len`` protocol and can be
iterated over as a sequence of hashable elements – in particular ``str`` and
``bytes``.  The return value is always an ``int``.
"""

from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    The distance is the minimum number of single‑character insertions,
    deletions or substitutions required to transform *a* into *b*.

    The implementation uses a two‑row dynamic programming table which gives
    O(len(a) * len(b)) time and O(min(len(a), len(b))) additional space.
    ``a`` and ``b`` may be any sequence type (strings, bytes, list of tokens …).
    """
    # Fast path for identical objects – also handles the empty‑string case.
    if a == b:
        return 0

    len_a, len_b = len(a), len(b)
    # If one of the strings is empty the distance is the length of the other.
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure that ``b`` is the shorter string – the inner loop iterates over ``b``.
    if len_b > len_a:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # ``previous`` holds the DP values for the row i‑1, ``current`` for row i.
    # Initialise the first row (transform empty ``a`` into prefixes of ``b``).
    previous = list(range(len_b + 1))
    current = [0] * (len_b + 1)

    # Iterate over each character of ``a``.
    for i in range(1, len_a + 1):
        # First column: converting ``a[:i]`` to empty ``b`` needs ``i`` deletions.
        current[0] = i
        ai = a[i - 1]

        # Compute the rest of the row.
        for j in range(1, len_b + 1):
            # Cost of substitution is 0 if characters match, otherwise 1.
            cost = 0 if ai == b[j - 1] else 1
            # Minimum of deletion, insertion, substitution.
            deletion = previous[j] + 1      # delete ai
            insertion = current[j - 1] + 1  # insert b[j-1]
            substitution = previous[j - 1] + cost
            current[j] = min(deletion, insertion, substitution)

        # Swap rows for next iteration – ``previous`` becomes the row we just
        # computed, ``current`` will be reused.
        previous, current = current, previous

    # After the final swap ``previous`` holds the last completed row.
    return previous[len_b]
