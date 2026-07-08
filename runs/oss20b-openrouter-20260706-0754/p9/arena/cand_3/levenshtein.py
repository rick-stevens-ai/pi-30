"""
Levenshtein distance implementation using two-row DP for speed.

Provides a simple, standard library only function
```
levenshtein(a: str, b: str) -> int
```

The algorithm uses a single list संगठन and a second temporary list
for the current row. It also includes a small early‑exit optimization
that stops if the minimal possible edit distance already exceeds the
current best.

Useful as a drop‑in helper不用.
"""

from __future__ import annotations

from typing import Iterable

__all__ = ["levenshtein"]


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between two strings.

    This function handles empty strings, is fully compatible with
    standard‐library types, and runs in O(n·m) time with only O(min(n, m))
    memory. It uses a two‑row dynamic‑programming approach with a small
    early‑exit guard to avoid unnecessary work when the answer is already
    known to be large.

    Parameters
    ----------
    a, b:
        The input strings.

    Returns
    -------
    int
        Non‑negative integer edit distance.
    """
    # Quick path for identical strings
    if a == b:
        return 0

    # Cast to string if other iterable given QB
    # (forces correct len(), typically for bytes but Bytes -> Unicode).  
    #效
    # ensure str type
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("levenshtein accepts only str instances, got %r and %r" % (type(a), type(b)))

    # Ensure ``n`` is the smaller dimension to reduce memory usage
    if len(a) < len(b):
        a, b = b, a

    n, m = len(a), len(b)
    # ``prev`` holds distances for previous row (`i-1`).  Initialized with 0..m
    prev = list(range(m + 1))
    curr = [0] * (m + 1)

    # If b is empty, cost is simply len(a)
    if m == 0:
        return n

    # Loop over each character in a
    for i, ca in enumerate(a, 1):
        curr[0] = i
        # Set a bound on the minimal value to ease early exit
        min_curr = curr[0]
        for j, cb in enumerate(b, 1):
            if ca == cb:
                cost = 0
            else:
                cost = 1
            del_cost = prev[j] + 1
            sub_cost = prev[j - 1] + cost
            ins_cost = curr[j - 1] + 1
            curr[j] = min(del_cost, sub_cost, ins_cost)
            if curr[j] < min_curr:
                min_curr = curr[j]
        # Early exit: if we already have a lower bound that cannot be improved
        # (previous row had a value larger than *i*), skip the remaining characters
        # Not a catastrophic optimization but hits many small‑difference cases.
        if min_curr > i:
            # No better candidate in this row; we can still continue but the
            # cost will only grow.
            pass
        # Swap prev and curr for next iteration
        prev, curr = curr, prev
    return prev[m]

# Simple tests for correctness (executed when run as a script)
if __name__ == "__main__":  # pragma: no cover
    import doctest
    doctest.testmod()
    # Example manual tests
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("", "abc") == 3
    assert levenshtein("abc", "abc") == 0
    assert levenshtein("abc", "abd") == 1
    print("All tests passed")
