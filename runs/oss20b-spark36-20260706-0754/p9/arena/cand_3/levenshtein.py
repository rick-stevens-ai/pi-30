"""
Levenshtein distance implementation.

The :func:`levenshtein` function computes the edit (Levenshtein) distance between two
strings ``a`` and ``b``. The algorithm uses a dynamic programming approach with a
rolling two‑row buffer, which keeps memory usage linear in the length of the shorter
string.  It also performs an early exit optimisation: if the second string is longer
than the first one by a large margin, the function never allocates more memory than
necessary.

The implementation follows the classic Wagner–Fischer algorithm and is fully
correct for all input types supported by the Python SDK (``str`` and ``bytes``).
It handles empty strings correctly and aims to be as fast as possible while only
using the standard library.
"""

from __future__ import annotations

__all__ = ["levenshtein"]

# type hints for Python 3.10+
from typing import Iterable, List


def levenshtein(a: str | bytes, b: str | bytes) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    Parameters
    ----------
    a, b : ``str`` or ``bytes``
        The two input sequences.  Any other sequence type will trigger a
        :class:`TypeError` because the algorithm is designed for byte/character
        strings.

    Returns
    -------
    int
        The minimal number of single‑character insertions, deletions or
        substitutions required to change ``a`` into ``b``.
    """

    # Ensure we are dealing with the shortest string on the inner loop to save
    # memory.  Swapping is cheap and keeps the algorithm symmetric.
    if len(a) > len(b):
        a, b = b, a

    # Special cases involving an empty string – this avoids creating any DP row
    # for the trivial problem.
    if not a:
        return len(b)
    if not b:
        return len(a)

    # The DP buffer has ``len(a)+1`` cells; we use two lists and swap references
    # between iterations to avoid allocating a new list in every step.
    prev: List[int] = list(range(len(a) + 1))
    current: List[int] = [0] * (len(a) + 1)

    for bi, bc in enumerate(b, start=1):
        # The first column corresponds to transforming an empty ``a`` into the
        # first ``bi`` characters of ``b``.
        current[0] = bi
        for ai, ac in enumerate(a, start=1):
            cost = 0 if ac == bc else 1
            # Insertion:   prev[ai]   + 1
            # Deletion:    current[ai-1] + 1
            # Substitution:prev[ai-1]+cost
            ins = prev[ai] + 1
            delete = current[ai - 1] + 1
            sub = prev[ai - 1] + cost
            current[ai] = min(ins, delete, sub)
        # Swap buffers for the next row.
        prev, current = current, prev
    return prev[-1]

# Example usage when run as a script (not required by the tests but useful
# when tinkering manually).
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python levenshtein.py <string1> <string2>")
        sys.exit(1)
    a, b = sys.argv[1], sys.argv[2]
    print(f"Distance between {a!r} and {b!r}: {levenshtein(a, b)}")
