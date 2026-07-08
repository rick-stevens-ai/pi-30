"""Introspective sort (introsort): quicksort with heapsort fallback.

This is the same family of algorithms used by C++ std::sort and by the
Python interpreter's own list sort (which is a stable, adaptive mergesort /
timsort variant). The implementation here is an explicit introsort so that
the "distinct angle" is the hand-rolled introspective hybrid rather than a
bare ``sorted`` call.

Guarantees
----------
- O(n log n) worst-case time (heapsort guards pathological quicksort).
- O(log n) recursion depth worst case (recurse only on the smaller side).
- In-place on a copy of the input, so the multiset of the original list is
  preserved exactly and the input is never mutated.
- Stable? No. Stability is *not* required: the contract is "new sorted list,
  ascending, preserving the multiset". Equality of values is all that matters.
- Works for empty lists, singletons, duplicates, negatives, and arbitrary
  big integers: comparisons use plain ``<`` which Python defines for all
  homogeneous numeric types, including unbounded ints.
"""

from __future__ import annotations

import sys
from math import log2
from typing import List, TypeVar

T = TypeVar("T")

# Below this size a partition is handed off to insertion sort, which has
# smaller constants and is cache-friendly for tiny runs.
_INSERTION_THRESHOLD = 24


def my_sort(xs: List[T]) -> List[T]:
    """Return a new list containing every element of ``xs`` in ascending order.

    The input list is never mutated; a shallow copy is sorted in place.
    """
    # ``list(xs)`` is a shallow copy: multiset is preserved, caller's list
    # is untouched. Handles iterables too, but the signature says List.
    a = list(xs)
    n = len(a)
    if n < 2:
        # Empty or singleton is already sorted. Also short-circuits the case
        # where xs is [] — no comparisons are attempted at all.
        return a

    # Recursion-depth ceiling. If quicksort's partitions become this unbalanced
    # we switch to heapsort to guarantee O(n log n). 2*log2(n) is the standard
    # introsort bound (cf. Musser 1997); a little extra headroom avoids
    # spurious fallbacks on already-sorted or nearly-sorted inputs, which
    # median-of-three handles well in practice.
    depth_limit = 2 * int(log2(n)) + 4
    _introsort(a, 0, n, depth_limit)
    return a


def _introsort(a: List[T], lo: int, hi: int, depth_limit: int) -> None:
    """Sort a[lo:hi] in place. ``hi`` is exclusive, ``lo`` inclusive."""
    while hi - lo > _INSERTION_THRESHOLD:
        if depth_limit == 0:
            # Quicksort recursion has gone too deep — degenerate partitions
            # are likely. Fall back to heapsort to keep the worst case at
            # O(n log n). Build a max-heap over the slice, then repeatedly
            # pop the max to the end.
            _heapsort(a, lo, hi)
            return

        depth_limit -= 1
        mid = _partition(a, lo, hi)
        # Tail-call elimination: recurse on the smaller side, loop on the
        # larger. Keeps recursion depth to O(log n).
        left_size = mid - lo
        right_size = hi - (mid + 1)
        if left_size < right_size:
            _introsort(a, lo, mid, depth_limit)
            lo = mid + 1
        else:
            _introsort(a, mid + 1, hi, depth_limit)
            hi = mid
    else:
        # Small slice: insertion sort. Loop exited because length <= threshold.
        _insertion_sort(a, lo, hi)


def _median_of_three(a: List[T], lo: int, hi: int) -> int:
    """Index of the median of a[lo], a[mid], a[hi-1].

    Median-of-three pivot selection kills the classic O(n^2) quicksort
    pathology on already-sorted / reverse-sorted / constant input — the
    inputs most likely to be handed to a general-purpose sort.
    """
    mid = lo + ((hi - lo) >> 1)
    x, y, z = a[lo], a[mid], a[hi - 1]
    if x < y:
        if y < z:
            return mid
        return lo if x < z else (hi - 1)
    else:  # y <= x
        if x < z:
            return lo
        return mid if y < z else (hi - 1)


def _partition(a: List[T], lo: int, hi: int) -> int:
    """Lomuto/Hoare-style partition around a median-of-three pivot.

    Returns the index ``p`` such that every element in ``a[lo:p]`` is
    strictly less than ``a[p]`` and every element in ``a[p+1:hi]`` is
    greater-or-equal. This three-way-ish split keeps duplicates from
    unbalancing the tree badly; combined with insertion sort on the
    tails it makes many-equal inputs run in ~linear time.

    Notably uses only ``<`` comparison, so it is well-defined for any
    total order Python defines — including ints of any magnitude, where
    there is no fixed-width wraparound to worry about.
    """
    pivot_idx = _median_of_three(a, lo, hi)
    pivot = a[pivot_idx]
    # Stash pivot at the front; we will find its final resting place.
    a[pivot_idx] = a[lo]
    a[lo] = pivot

    # Hoare-style two-pointer scan.
    i = lo
    j = hi
    while True:
        i += 1
        while i < hi and a[i] < pivot:
            i += 1
        j -= 1
        while j >= lo and pivot < a[j]:
            j -= 1
        if i >= j:
            break
        a[i], a[j] = a[j], a[i]

    # Put pivot back into the gap. Everything left of j is < pivot (or equal),
    # everything from j onward is >= pivot.
    a[lo] = a[j]
    a[j] = pivot
    return j


def _insertion_sort(a: List[T], lo: int, hi: int) -> None:
    """Straight insertion sort on a[lo:hi]. Excellent for tiny slices."""
    for i in range(lo + 1, hi):
        key = a[i]
        j = i - 1
        # Single comparison form; ``<`` keeps it correct for big ints.
        while j >= lo and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


def _heapsort(a: List[T], lo: int, hi: int) -> None:
    """In-place heapsort on a[lo:hi] (max-heap, then drain)."""
    n = hi - lo

    # Build a max-heap (Floyd's linear-time build).
    # Parent index relative to ``lo``: (i-1)//2 ; children: 2i+1, 2i+2.
    start = n // 2 - 1
    for parent in range(start, -1, -1):
        _sift_down(a, lo, parent, n)

    # Repeatedly move the current max to the end and shrink the heap.
    for end in range(n - 1, 0, -1):
        a[lo], a[lo + end] = a[lo + end], a[lo]
        _sift_down(a, lo, 0, end)


def _sift_down(a: List[T], base: int, root: int, size: int) -> None:
    """Restore the max-heap invariant for a[root] within a heap of ``size``.

    Indices are relative offsets from ``base``.
    """
    # Iterative sift-down avoids Python recursion overhead and stack growth.
    while True:
        child = 2 * root + 1  # left child
        if child >= size:
            return
        right = child + 1
        # Pick the larger child so the heap is a *max*-heap.
        if right < size and a[base + child] < a[base + right]:
            child = right
        if a[base + child] < a[base + root]:
            # Invariant already holds.
            return
        a[base + root], a[base + child] = a[base + child], a[base + root]
        root = child


def _self_test() -> None:  # pragma: no cover - sanity check at import time
    import random
    rng = random.Random(12345)

    cases: List[List[object]] = [
        [],
        [1],
        [2, 1],
        [1, 1, 1],
        [-5, -1, -9, 0, 3, -3],
        [10**18, -(10**18), 0, 10**18 + 1, -(10**18) - 1],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        list(range(20)),
        list(range(20, 0, -1)),
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        [0, -0, 1, -1, 2, -2],
        [2**64, 2**64 - 1, 2**64 + 1, -(2**64), 1, 0],
    ]
    for c in cases:
        got = my_sort(c)
        expected = sorted(c)
        assert got == expected, (c, got, expected)
        # Input must be unmutated.
        assert list(c) == c

    big = [rng.randrange(-1_000_000, 1_000_000) for _ in range(200_000)]
    assert my_sort(big) == sorted(big)

    print("my_sort: all self-tests passed")


if __name__ == "__main__":
    _self_test()
