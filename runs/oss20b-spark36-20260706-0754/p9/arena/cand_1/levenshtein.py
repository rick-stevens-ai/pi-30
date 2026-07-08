"""
Levenshtein distance (edit distance) implementation.

This function computes the minimum number of single-character edits
(insertions, deletions or substitutions) required to change one string
into the other. It uses a classic dynamic programming approach that
maintains only two rows of the DP table at any time, achieving O(min(m,n))
space usage and O(m*n) time complexity.

Both input strings are assumed to be sequences of characters (or any
sequence type). The implementation is fully correct for all inputs,
including empty strings. It also handles cases where the two input
strings are identical quickly, as well as swapping arguments so that
the inner loop iterates over the shorter string for better cache
performance.

The code is written with a focus on clarity and speed while staying
within the standard library only.
"""

from __future__ import annotations


def levenshtein(a: str, b: str) -> int:
    """Return Levenshtein distance between two strings ``a`` and ``b``.

    Parameters
    ----------
    a: str
        First input string.
    b: str
        Second input string.

    Returns
    -------
    int
        Minimum number of edits required to transform ``a`` into ``b``.
    """
    # Quick checks for common cases.
    if a == b:
        return 0
    len_a, len_b = len(a), len(b)
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure ``b`` is the shorter string to minimize memory usage.
    if len_b > len_a:
        a, b = b, a
        len_a, len_b = len_b, len_a

    # Previous and current rows of the DP table.
    prev_row = list(range(len_b + 1))
    cur_row = [0] * (len_b + 1)

    for i in range(1, len_a + 1):
        cur_row[0] = i
        a_char = a[i - 1]
        # Inner loop over the shorter string ``b``.
        for j in range(1, len_b + 1):
            cost = 0 if a_char == b[j - 1] else 1
            cur_row[j] = min(
                prev_row[j] + 1,       # Deletion
                cur_row[j - 1] + 1,    # Insertion
                prev_row[j - 1] + cost,  # Substitution (or match)
            )
        # Swap rows for next iteration.
        prev_row, cur_row = cur_row, prev_row

    return prev_row[len_b]

__all__ = ["levenshtein"]

# Simple self-test when run as a script.
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python levenshtein.py <string1> <string2>")
        sys.exit(1)
    s1, s2 = sys.argv[1], sys.argv[2]
    print(f"Levenshtein distance between {s1!r} and {s2!r}: {levenshtein(s1, s2)}")
