"""levenshtein.py

A tiny, dependency‑free implementation of the Levenshtein edit distance.

The public API consists of a single function:

    levenshtein(a: str, b: str) -> int

It returns the minimum number of single‑character insertions, deletions or
substitutions required to transform *a* into *b*.

The implementation uses the classic two‑row dynamic‑programming algorithm
which runs in O(len(a) * len(b)) time while only allocating O(min(len(a),
len(b))) additional space.  An early‑exit optimisation is applied when the
absolute length difference between the strings already exceeds the best
possible distance found so far; in that case we can immediately return the
difference because each extra character forces at least one edit.

Only the Python standard library is used.
"""

from __future__ import annotations

__all__ = ["levenshtein"]


def _swap_if_needed(a: str, b: str) -> tuple[str, str, bool]:
    """Return ``(short, long, swapped)`` where *short* is the shorter string.

    The DP algorithm works on the shorter string as the *columns* to keep the
    auxiliary row as small as possible.  The ``swapped`` flag indicates whether
    the inputs were swapped – it is only used for debugging or future
    extensions and does not affect the numerical result.
    """
    if len(a) <= len(b):
        return a, b, False
    else:
        return b, a, True


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein distance between *a* and *b*.

    Parameters
    ----------
    a, b:
        Input strings.  They may be empty.

    Returns
    -------
    int
        The edit distance.
    """
    # Fast path for the trivial cases.
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure ``short`` is the shorter of the two strings – this keeps the
    # auxiliary row minimal.
    short, long, _ = _swap_if_needed(a, b)
    n, m = len(short), len(long)

    # If the length difference already exceeds the minimum possible distance
    # we can return it straight away.
    length_diff = abs(len(a) - len(b))
    if length_diff == 0:
        # No early exit possible – continue with DP.
        pass
    else:
        # The distance cannot be smaller than ``length_diff``.  The DP loop
        # will never produce a value below this threshold, so we keep it as a
        # lower bound for early termination.
        lower_bound = length_diff
    # Initialise the first row (transforming the empty prefix of ``short``
    # into prefixes of ``long``).
    previous = list(range(m + 1))
    current = [0] * (m + 1)

    for i in range(1, n + 1):
        current[0] = i  # cost of deleting i characters from ``short``
        # Track the minimal value in the current row for early exit.
        row_min = current[0]
        ch = short[i - 1]
        for j in range(1, m + 1):
            # Cost of substitution: 0 if chars match, 1 otherwise.
            substitution_cost = 0 if ch == long[j - 1] else 1
            # Compute the three possible operations.
            insert = current[j - 1] + 1          # insertion
            delete = previous[j] + 1             # deletion
            replace = previous[j - 1] + substitution_cost  # substitution
            current[j] = min(insert, delete, replace)
            # Keep track of the smallest cell value in this row.
            if current[j] < row_min:
                row_min = current[j]
        # Early exit: if the smallest value in this row already exceeds the
        # lower bound (which is the minimal distance forced by length diff),
        # we cannot improve it any further.
        if length_diff and row_min > lower_bound:
            return length_diff + (row_min - lower_bound)
        # Prepare for next iteration.
        previous, current = current, previous

    # The last populated ``previous`` row holds the final distances.
    return previous[m]
