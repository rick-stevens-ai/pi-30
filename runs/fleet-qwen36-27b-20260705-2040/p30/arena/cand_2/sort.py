"""
sort.py — Iterative bottom-up merge sort with insertion-sort cutoff.

Distinct angle: instead of recursive top-down divide-and-conquer, this
builds the sorted result from the bottom up by repeatedly merging adjacent
runs of increasing width (1, 2, 4, 8, …).  Small runs are first sorted in
place via insertion sort, which is faster than merging for tiny segments.

Properties
----------
* Stability:    stable (equal elements keep their original order)
* Time:         O(n log n) worst-case
* Space:        O(n) for the auxiliary buffer
* Recursion:    none — safe for arbitrarily large inputs
* Correctness:  preserves the multiset exactly; handles empty, singletons,
                duplicates, negatives, big ints, and mixed-comparable types.
"""

from __future__ import annotations

INSERTION_CUTOFF = 32  # runs smaller than this are sorted by insertion sort


def _insertion_sort(buf: list, lo: int, hi: int) -> None:
    """Sort buf[lo:hi] in-place using insertion sort."""
    for i in range(lo + 1, hi):
        key = buf[i]
        j = i - 1
        while j >= lo and buf[j] > key:
            buf[j + 1] = buf[j]
            j -= 1
        buf[j + 1] = key


def my_sort(xs: list) -> list:
    """Return a new list containing the elements of *xs* in ascending order.

    Uses an iterative bottom-up merge sort with an insertion-sort
    pre-pass for small runs.  Stdlib only, O(n log n) worst-case.
    """
    n = len(xs)
    if n <= 1:
        return list(xs)

    # Work on a copy so the original is never mutated.
    buf = list(xs)

    # Phase 1 — sort small runs in-place via insertion sort.
    # This produces a buffer that is already partially ordered, which
    # makes the subsequent merge passes much cheaper.
    run = INSERTION_CUTOFF
    for start in range(0, n, run):
        end = min(start + run, n)
        _insertion_sort(buf, start, end)

    # Phase 2 — iterative bottom-up merging.
    # width is the size of each run to merge; doubles each pass.
    aux = [None] * n  # pre-allocate auxiliary buffer
    width = INSERTION_CUTOFF
    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)
            if mid < right:
                _merge(buf, aux, left, mid, right)
        width *= 2

    return buf


def _merge(buf: list, aux: list, left: int, mid: int, right: int) -> None:
    """Merge two adjacent sorted runs buf[left:mid] and buf[mid:right]
    into aux, then copy the merged segment back into buf."""
    i, j = left, mid

    # Copy merged result into aux[left:right].
    k = left
    while i < mid and j < right:
        if buf[i] <= buf[j]:  # '<=' preserves stability
            aux[k] = buf[i]
            i += 1
        else:
            aux[k] = buf[j]
            j += 1
        k += 1

    # Drain remaining elements (only one of these loops runs).
    while i < mid:
        aux[k] = buf[i]
        i += 1
        k += 1
    while j < right:
        aux[k] = buf[j]
        j += 1
        k += 1

    # Copy back.
    buf[left:right] = aux[left:right]
