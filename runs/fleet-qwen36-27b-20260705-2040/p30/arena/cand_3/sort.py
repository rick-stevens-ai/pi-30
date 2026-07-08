"""
Iterative bottom-up merge sort — no recursion, stable, O(n log n).

Distinct angle:  uses a single auxiliary buffer and alternates the
"source" direction each pass so we never copy data back and forth.
This halves the memory traffic compared to a naive merge-sort that
allocates a new list per merge.
"""

from __future__ import annotations
from typing import List, TypeVar

T = TypeVar("T")


def my_sort(xs: List[T]) -> List[T]:
    """Return a new list containing the same elements as *xs* in ascending order."""
    n = len(xs)
    if n <= 1:
        return list(xs)  # copy, never mutate input

    # Work on a copy so the original is untouched.
    left = list(xs)       # first pass: merge into right
    right = [None] * n    # second pass: merge back into left, etc.

    width = 1  # current run length; doubles each pass

    while width < n:
        # Merge runs of length *width* from `left` into `right`.
        i = 0
        while i < n:
            lo = i
            mid = min(i + width, n)
            hi = min(i + 2 * width, n)
            _merge(left, right, lo, mid, hi)
            i = hi
        # Swap roles: right becomes the source for the next pass.
        left, right = right, left
        width *= 2

    # After the loop the fully-sorted data lives in `left`.
    return left


def _merge(src: List[T], dst: List[T], lo: int, mid: int, hi: int) -> None:
    """Merge two adjacent sorted runs *src[lo:mid]* and *src[mid:hi]*
    into *dst[lo:hi]* in-place (within dst)."""
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
    # Copy remaining elements (only one of these loops runs).
    while i < mid:
        dst[k] = src[i]
        i += 1
        k += 1
    while j < hi:
        dst[k] = src[j]
        j += 1
        k += 1
