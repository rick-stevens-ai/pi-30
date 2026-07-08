"""
Levenshtein edit distance implementation.

Provides a single function `levenshtein(a: str, b: str) -> int` that returns the
edit (Hamming) distance between two strings. The implementation uses a classic
two‑row dynamic programming algorithm and includes a couple of trivial speed
optimisations:

* If the input strings are equal, zero is returned immediately.
* Empty string handling is short‑circuited.
* The inner DP array size is set to the length of the shorter string, so that
  space usage is minimal.

The code has no external dependencies and should run efficiently for all
reasonable input sizes.
"""
from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    Parameters
    ----------
    a, b
        The two input strings.  Both may be empty.

    Returns
    -------
    int
        Non‑negative integer equal to the minimum number of insertions,
        deletions, or substitutions required to transform *a* into *b*.

    Notes
    -----
    This implementation has a time complexity of :math:`O(n\cdot m)` where
    ``n`` and ``m`` are the lengths of the input strings, but only uses
    :math:`O(min(n,m))` additional space thanks to the two‑row DP approach.
    """
    # Short circuit trivial cases
    if a == b:
        return 0

    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la

    # It is more efficient to have the inner loop iterate over the shorter
    # string.  This reduces the size of the DP rows.
    if lb > la:
        a, b = b, a
        la, lb = lb, la

    # Two row DP: ``prev`` holds distances for the previous character in ``a``
    # and ``curr`` is built iteratively.
    prev = list(range(lb + 1))  # initialised to 0 .. lb (empty '' -> prefix of b)
    curr = [0] * (lb + 1)

    for i, ca in enumerate(a, start=1):
        curr[0] = i  # Cost of deleting all characters from ``a``'s prefix.
        for j, cb in enumerate(b, start=1):
            deletion = prev[j] + 1
            insertion = curr[j - 1] + 1
            substitution = prev[j - 1] + (ca != cb)
            curr[j] = min(deletion, insertion, substitution)
        # Prepare for next iteration.
        prev, curr = curr, prev
    return prev[lb]

*** End of file ***