"""Levenshtein distance implementation.

This module provides a single function :func:`levenshtein` which computes the
edit distance between two strings using a two‑row dynamic programming table.

It works correctly for all inputs including empty strings, and it uses only
Python's standard library.  The implementation is optimised for speed by
always iterating over the shorter input as the outer loop.

Example
-------
>>> levenshtein("kitten", "sitting")
3
"""

from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    The algorithm uses a classic dynamic‑programming approach that keeps only
    two rows of the DP matrix in memory, resulting in a space complexity of
    :math:`O(min(len(a), len(b)))`.

    Parameters
    ----------
    a, b: str
        Input strings.

    Returns
    -------
    int
        The edit distance.
    """
    # Turn the inputs into sequences of characters.  In case a or b are
    # not strings (e.g. bytes), we convert to ``str``.
    s = str(a)
    t = str(b)

    # If both are empty, the distance is 0.
    if not s:
        return len(t)
    if not t:
        return len(s)

    # For performance, iterate over the shorter string in the outer loop.
    if len(s) > len(t):
        s, t = t, s
    # Now len(s) <= len(t)
    len_s, len_t = len(s), len(t)

    # Previous row: distance of prefixes of ``t`` against the empty prefix of ``s``.
    prev = list(range(len_t + 1))
    # Current row placeholder.  Reuse a list for speed.
    curr = [0] * (len_t + 1)

    for i, sc in enumerate(s, 1):
        curr[0] = i  # cost of deleting all characters of ``s`` up to i
        for j, tc in enumerate(t, 1):
            cost_sub = 0 if sc == tc else 1
            # Compute distances for delete, insert, substitute
            del_cost = prev[j] + 1
            ins_cost = curr[j - 1] + 1
            sub_cost = prev[j - 1] + cost_sub
            curr[j] = min(del_cost, ins_cost, sub_cost)
        # After finishing the inner loop, swap rows.
        prev, curr = curr, prev
    # The final answer is in ``prev`` after the last swap.
    return prev[len_t]


# If run as a script, perform a simple test.
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: levenshtein.py str1 str2")
    else:
        print(levenshtein(sys.argv[1], sys.argv[2]))
