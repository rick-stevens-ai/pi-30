"""Candidate #2 — Three-way Quicksort with median-of-three pivoting.

Stdlib-only, O(n log n) average / two-key partitions collapse equal keys in
one pass (Dutch National Flag), so duplicates are "for free".  Hybrid: falls
back to heapsort for deep recursion to guarantee worst-case, and short-runs
switch to insertion sort for cache locality.

Returns a NEW sorted list; input is never mutated.
"""

from __future__ import annotations


def my_sort(xs):
    """Return *xs* sorted into a new ascending list (multiset-preserving)."""
    # --- empty / singleton are identity-copies by construction below ---
    if not xs:
        return []
    a = list(xs)                       # fresh copy — caller never sees mutation
    _quicksort(a, 0, len(a) - 1)       # in-place on the copy
    return a


# ── internal helpers ────────────────────────────────────────────────
def _quicksort(a: list, lo: int, hi: int) -> None:
    """Three-way quicksort with depth guard → heap-sort fallback."""
    LIMIT = len(a).bit_length() + 1   # 2·log₂(n) ≈ worst-case limit

    while lo < hi and LIMIT > 0:
        LIMIT -= 1                       # borrow two levels of credit each turn

        # --- small window: insertion sort — fewer comparisons & moves ---
        if hi - lo < 64:
            _insertion_sort(a, lo, hi)
            return

        # pick pivot (median-of-three)
        pivot = _median_of_three(a, lo, hi)

        # Dutch-National-Flag partition: [lo..lt-1] < pivot == eq[0]] > ]>a[gt .. hi]
        lt, gt = _three_way_partition(a, lo, hi, pivot)

        # recurse on the unequal halves; skip the equal middle — O(d) not O(n)
        if len(a) - lo > 10**6 and len(a) - gt > 10**6:
            # defer smaller partition to keep stack depth logarithmic
            _quicksort(a, lo, lt - 1)       # recurse left (deeper) first — loop unrolls right side
            lo = gt + 1                    # tail-call → while-loop iteration
        else:
            _quicksort(a, lo, lt - 1)      # recurse both sides in-order; stack depth bounded by LIMIT
            _quicksort(a, gt + 1, hi)

    # if we exhausted budget, fall back to guaranteed O(n log n) heapsort
    if lo < hi:
        _heapsort(a, lo, hi)


def _swap(a, i, j):
    """Swap a[i] and a[j] in place."""
    if i != j:
        a[i], a[j] = a[j], a[i]


def _median_of_three(a, lo, hi):
    """Return the median-of-values among a[lo], a[mid], a[hi]."""
    mid = (lo + hi) // 2
    x, y, z = a[lo], a[mid], a[hi]
    # Sort three values and pick the middle one
    if x > y:
        if x < z:
            pivot = x
        elif y < z:
            pivot = z
        else:
            pivot = y
    elif y > z:
        if x > z:
            pivot = x
        else:
            pivot = z
    else:
        pivot = y
    return pivot


def _three_way_partition(a, lo, hi, pivot):
    """Dutch National Flag: partition in-place into 3 zones.

    Returns (lt, gt) where:
      a[lo .. lt-1] <  pivot
      a[lt ..   gt] == pivot            ← collapsed equal keys
      a[gt+1 .. hi] >  pivot
    """
    # swap median to position lo for canonical DNF layout
    _swap(a, lo, lo + (hi - lo) // 2)
    lt = lo                            # boundary of "< pivot" zone
    gt = hi                            # boundary of "> pivot" zone
    i = lo + 1                         # scan pointer

    while i <= gt:
        if a[i] < pivot:
            _swap(a, lt, i)
            lt += 1
            i += 1
        elif a[i] > pivot:
            _swap(a, i, gt)
            gt -= 1                   # don't advance i — re-examine dropped element
        else:                          # a[i] == pivot → skip; it's already in the middle zone
            i += 1

    return lt, gt                      # equal-zone covers [lt..gt]; next recurse bounds


def _insertion_sort(a, lo, hi):
    """Straight insertion sort on a[lo .. hi]."""
    for i in range(lo + 1, hi + 1):
        key = a[i]
        j = i - 1
        while j >= lo and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


def _heapsort(a, lo, hi):
    """Bottom-up heapsort as worst-case guarantee.

    Operates in-place on the given slice; uses standard sifting from bottom up
    then repeatedly extracts max to the tail position.
    """
    # heapify the range [lo..hi]  (bottom-up, right-to-left sift-down)
    for start in range((hi - lo) // 2 + lo, lo - 1, -1):
        _siftdown(a, lo, hi, start)

    sink = hi                          # write-back slot (shrinks from the tail)
    while sink > lo:
        _swap(a, lo, sink)             # move max to end of heap range
        sink -= 1
        if sink <= lo:
            break                     # single remaining element → done
        _siftdown(a, lo, sink, lo)    # restore heap property


def _siftdown(a, lo, hi, start):
    """Sift down node at `start` inside [lo..hi].  Largest-wins (max-heap)."""
    while True:
        left_child = 2 * start + 1
        right_child = left_child + 1
        largest = start

        if left_child <= hi and a[left_child] > a[largest]:
            largest = left_child
        if right_child <= hi and a[right_child] > a[largest]:
            largest = right_child

        if largest == start:
            break                        # heap property restored
        _swap(a, start, largest)
        start = largest                  # continue sifting down

