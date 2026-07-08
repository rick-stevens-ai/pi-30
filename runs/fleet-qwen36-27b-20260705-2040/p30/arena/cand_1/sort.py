"""Bottom-up iterative mergesort — stable, O(n log n), stdlib-only."""

from __future__ import annotations


def my_sort(xs: list) -> list:
    """Return a new list containing the elements of *xs* in ascending order.

    Uses a bottom-up (iterative) mergesort: repeatedly merge adjacent
    runs of width *w* (1, 2, 4, 8, …) until the entire list is covered.

    Properties
    ----------
    * Stable — equal elements keep their original relative order.
    * O(n log n) worst-case comparisons and moves.
    * O(n) auxiliary space (one extra buffer the size of *xs*).
    * No recursion — safe for arbitrarily large inputs.
    * Handles any comparable type (ints, floats, strings, big ints, …).
    """
    n = len(xs)
    if n <= 1:
        return list(xs)

    buf = list(xs)  # working copy; we alternate between xs and buf as read/write

    # Merge runs of width `w` into runs of width `2*w`.
    # After each pass, the sorted data lives in `buf`.
    w = 1
    while w < n:
        for i in range(0, n, 2 * w):
            lo = i
            mid = min(i + w, n)
            hi = min(i + 2 * w, n)
            _merge(xs, buf, lo, mid, hi)
        w *= 2
        # Swap roles: buf now holds the sorted pass, becomes the source.
        xs, buf = buf, xs

    # The final sorted data may be in `buf` if the last swap left it there.
    # We always return the contents of `xs` (which holds the latest pass)
    # *unless* the number of passes was even, in which case it's in `buf`.
    # Easiest: just copy from whichever has the final result.
    # After the loop, `xs` holds the data if the number of passes was odd,
    # otherwise `buf` does. We can detect this by checking if the last swap
    # happened.  Simpler: just return list(xs) — the roles are swapped each
    # iteration, so the final result is in `xs` when the loop exits with
    # `w >= n`.  Let's trace:
    #   pass 1: merge into buf, swap → xs=sorted, buf=old
    #   pass 2: merge into buf, swap → xs=sorted, buf=old
    #   ... each pass ends with sorted data in xs.
    # So xs always holds the result after the loop.
    return list(xs)


def _merge(src: list, dst: list, lo: int, mid: int, hi: int) -> None:
    """Merge src[lo:mid] and src[mid:hi] (both sorted) into dst[lo:hi]."""
    i, j = lo, mid
    k = lo
    while i < mid and j < hi:
        if src[i] <= src[j]:  # <= preserves stability
            dst[k] = src[i]
            i += 1
        else:
            dst[k] = src[j]
            j += 1
        k += 1
    # Drain remaining elements (at most one side has leftovers).
    while i < mid:
        dst[k] = src[i]
        i += 1
        k += 1
    while j < hi:
        dst[k] = src[j]
        j += 1
        k += 1
