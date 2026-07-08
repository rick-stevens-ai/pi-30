"""
Levenshtein distance implementation.

This module exposes :func:`levenshtein` which computes the edit distance
between two strings using a highly optimised, two‑row dynamic programming
approach.  The algorithm is O(len(a) * len(b)) time and O(min(len(a),
len(b))) space.

The implementation accepts all string inputs including empty strings and
returns an integer representing the number of single‑character edits
(insertion, deletion or substitution) required to transform ``a`` into
``b``.
"""

from __future__ import annotations


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein distance between *a* and *b*.

    The algorithm uses a one‑dimensional DP array of size ``min(len(a),
    len(b)) + 1`` to maintain the previous row while iterating over the
    longer string.  Early exit is achieved for identical strings or when
    one operand is empty.

    Parameters
    ----------
    a, b:
        Input strings.

    Returns
    -------
    int
        Number of edit operations (insertion, deletion, substitution).
    """

    if a == b:
        return 0

    la, lb = len(a), len(b)
    if not la:
        return lb
    if not lb:
        return la

    # Ensure the second string is the shorter one to minimise memory.
    if lb > la:
        a, b = b, a
        la, lb = lb, la

    previous_row = list(range(lb + 1))

    for i in range(1, la + 1):
        current_first = i
        prev_diag = previous_row[0]  # value from previous row, col j-1
        current_row = [current_first]
        ch_a = a[i - 1]
        for j in range(1, lb + 1):
            cost = 0 if ch_a == b[j - 1] else 1
            # substitutions/detections from previous row
            delete_cost = previous_row[j] + 1
            insert_cost = current_row[-1] + 1
            replace_cost = prev_diag + cost
            curr_val = min(delete_cost, insert_cost, replace_cost)
            current_row.append(curr_val)
            prev_diag = previous_row[j]
        previous_row = current_row
    return previous_row[-1]

# Example usage:
if __name__ == "__main__":  # pragma: no cover
    import doctest
    doctest.testmod()
"