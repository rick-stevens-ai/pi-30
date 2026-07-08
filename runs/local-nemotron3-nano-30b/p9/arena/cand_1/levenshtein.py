"""Levenshtein distance (edit distance) implementation using two‑row DP.

The function `levenshtein(a, b)` returns the minimum number of single‑character
insertions, deletions, or substitutions required to transform string ``a`` into
string ``b``.  It correctly handles empty inputs and runs in O(len(a)·len(b))
time with only O(min(len(a), len(b))) additional space.

Only Python's standard library is used.
"""

from typing import List


def levenshtein(a: str, b: str) -> int:
    """
    Compute the Levenshtein edit distance between two strings.

    Parameters
    ----------
    a : str
        First string (may be empty).
    b : str
        Second string (may be empty).

    Returns
    -------
    int
        The minimum number of edits required to turn ``a`` into ``b``.
    """
    # Quick checks for identity or emptiness
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Ensure that `a` is the shorter string to minimise allocation size
    if len(a) > len(b):
        a, b = b, a

    # Two rows of DP: previous (i‑1) and current (i)
    previous: List[int] = list(range(len(a) + 1))
    current: List[int] = [0] * (len(a) + 1)

    for i, ch_b in enumerate(b, start=1):
        # The cost of turning an empty prefix into the first i characters of b
        current[0] = i

        # Early exit optimization: if `current[0]` already exceeds the length of `a`,
        # we cannot get a better result than simply returning it (the distance is
        # at least this value).  This early check can avoid unnecessary inner loops.
        limit = len(a)
        if current[0] > limit:
            # The edit distance will be larger anyway, but we still need the final
            # answer, so continue computation.  Returning here would be incorrect,
            # thus no early return — just keep computing.
            pass

        for j, ch_a in enumerate(a, start=1):
            cost = 0 if ch_a == ch_b else 1
            current[j] = min(
                previous[j] + 1,          # deletion from b
                current[j - 1] + 1,       # insertion into a
                previous[j - 1] + cost    # substitution / match
            )
        # Swap rows for next iteration
        previous, current = current, previous

    return previous[-1]


if __name__ == "__main__":
    # Simple sanity checks
    assert levenshtein("", "") == 0
    assert levenshtein("a", "") == 1
    assert levenshtein("", "test") == 4
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("flaw", "lawn") == 2
    print("All internal tests passed.")