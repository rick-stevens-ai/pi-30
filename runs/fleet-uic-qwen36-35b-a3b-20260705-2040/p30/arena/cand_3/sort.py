"""Candidate #3 — bottom-up (iterative) merge sort.

Distinct angle: recursive merge-sorts dive & conquer; this goes the other way,
starting from length-(min_run) runs that are sorted in-place via binary-insertion,
then iteratively merges adjacent runs upward until one sorted list remains.
No recursion depth risk, O(n log n) guaranteed, stable, preserves multiset.

Stdlib only — uses bisect for the small-run insertion stage.
"""

from __future__ import annotations

import sys
from typing import Sequence, TypeVar
from bisect import insort_left

T = TypeVar("T")


def _bin_ins_sort(arr: list[T], lo: int, hi: int) -> None:
    """Insertion-sort via binary search for the window arr[lo..hi]."""
    for start in range(lo + 1, hi + 1):
        key = arr[start]
        # find insertion index among already-sorted prefix arr[lo..start-1]
        left, right = lo, start - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] > key:       # strictly greater → slide towards lo
                right = mid - 1
            else:
                left = min_run_size = mid + 1
        # shift elements [ins..start-1] one step right, then place key
        for idx in range(start, left - 1, -1):
            arr[idx] = arr[idx - 1]
        arr[left] = key


def my_sort(xs: Sequence[T]) -> list[T]:
    """Return a **new** ascending-sorted list (multiset-preserving)."""

    n = len(xs)
    if n <= 1:
        return [*xs]                        # copy; handles [] and [x]

    out = list(xs)                          # mutable copy to sort in place

    min_run_size = max(7, n ** (1 / 3))     # sweet spot from PigeonSort
    min_run_size = int(min_run_size)

    # --- Step 1: build sorted runs of size ≈ min_run via binary insertion ----
    lo = 0
    while lo < n:
        run_end = min(lo + min_run_size, n) - 1
        _bin_ins_sort(out, lo, run_end)
        lo = run_end + 1

    # --- Step 2: iteratively merge adjacent runs (2× widen each pass) ---------
    width = min_run_size
    while width < n:
        lo = 0
        while lo < n:
            mid = lo + width                  # start of right run
            rhi = min(lo + 2 * width, n)      # end of second run (clamped)

            if mid < rhi:                     # only merge when two runs exist
                _merge(out, lo, mid, rhi)

            lo += 2 * width                   # skip past the merged block
        width *= 2                            # double for next sweep

    return out


def _merge(a: list[T], lo: int, mid: int, hi: int) -> None:
    """Stably merge a[lo..mid-1] and a[mid..hi] in-place via auxiliary array."""
    left = a[lo:mid]             # slice is a copy (stdlib only)
    right = a[mid:hi]

    i, j, k = 0, 0, lo          # write-back position starts at lo
    len_l, len_r = len(left), len(right)

    while i < len_l and j < len_r:
        if left[i] <= right[j]:  # <= keeps it stable on ties
            a[k] = left[i]
            i += 1
        else:
            a[k] = right[j]
            j += 1
        k += 1

    while i < len_l:
        a[k] = left[i]
        i += 1
        k += 1

    # remaining right elements — drain too (at most one loop fires)
    while j < len_r:
        a[k] = right[j]
        j += 1
        k += 1


if __name__ == "__main__":                        # quick smoke test
    import random
    assert my_sort([]) == []
    assert my_sort([42]) == [42]
    assert my_sort([-3, -1, -7, 0, 5]) ==[-7, -3, -1, 0, 5]
    assert my_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    assert my_sort([10**18, -10**18, 0]) == [-10**18, 0, 10**18]

    SIZE = 2_000_000
    data = [random.randrange(-SIZE * 2, SIZE * 3) for _ in range(SIZE)]
    expected = sorted(data)                       # truth oracle (C-optimized Timsort)
    got = my_sort(data)
    assert got == expected, "FAIL on large random"         # should pass

    print(f"all OK — n={SIZE} ✓")
