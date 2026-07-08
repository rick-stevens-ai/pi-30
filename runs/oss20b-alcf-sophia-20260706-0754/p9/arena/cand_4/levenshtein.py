"""
Levenshtein distance implementation using a two‑row dynamic programming
approach with early exit optimization.

The algorithm runs in O(min(len(a), len(b))) extra memory and O(len(a) * len(b)) time.
It works for any hashable sequence of hashable elements, but for typical use
cases it treats strings as sequences of characters.

Typical usage::

    from levenshtein import levenshtein
    d = levenshtein("kitten", "sitting")
    assert d == 3

"""

from __future__ import annotations

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    The implementation uses a classic dynamic programming algorithm
    that keeps only two rows of the full DP matrix, thus using
    O(min(len(a), len(b))) additional memory.

    Parameters
    ----------
    a, b : str
        The input strings.

    Returns
    -------
    int
        Non‑negative edit distance.

    The function handles empty inputs correctly, exploits the early
    exit when the strings are identical, and also switches the shorter
    string to be the inner loop to minimise the number of iterations.
    """

    # Fast exit for identical strings
    if a == b:
        return 0

    # Ensure a is the shorter string to keep the DP array minimal
    if len(a) > len(b):
        a, b = b, a

    len_a, len_b = len(a), len(b)
    if len_a == 0:
        return len_b

    # Initialise the previous row with 0..len_a
    prev_row = list(range(len_a + 1))
    curr_row = [0] * (len_a + 1)

    # Iterate over characters of longer string (b)
    for i in range(1, len_b + 1):
        curr_row[0] = i
        bi = b[i - 1]
        # Local variable for speed
        prev_val = prev_row[0]
        for j in range(1, len_a + 1):
            # Cost of substitution
            cost = 0 if bi == a[j - 1] else 1
            # Compute minimum edit distance for this cell
            del_cost = prev_row[j] + 1
            ins_cost = curr_row[j - 1] + 1
            sub_cost = prev_val + cost
            curr_val = del_cost if del_cost <= ins_cost else ins_cost
            if sub_cost < curr_val:
                curr_val = sub_cost
            curr_row[j] = curr_val
            prev_val = prev_row[j]
        # Swap rows for next iteration
        prev_row, curr_row = curr_row, prev_row

    return prev_row[len_a]


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python levenshtein.py <string1> <string2>")
        sys.exit(1)
    a, b = sys.argv[1], sys.argv[2]
    print(levenshtein(a, b))
