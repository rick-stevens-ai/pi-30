"""Sort using QuickSort with median-of-three pivot, three-way partitioning,
and insertion-sort cutoff for small subarrays.

Distinct angle: a divide-and-conquer approach with excellent cache locality and
O(n log n) average-case performance. Three-way (Dutch National Flag) partitioning
handles duplicate-heavy data efficiently in a single pass — unlike two-way which
degrades to O(n^2) on arrays of all equal elements.

Preserves multiset: every element appears the same number of times as input.
"""


def _insort(arr, lo, hi):
    """Insertion sort for small subarrays (in-place on *arr* slice)."""
    while hi - lo > 16:
        mid = (hi + lo) // 2
        if arr[mid] < arr[lo]:
            hi = mid
        else:
            lo = mid
    # Insertion sort the final ~16 elements
    for i in range(lo + 1, hi + 1):
        key = arr[i]
        j = i - 1
        while j >= lo and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def _three_way_partition(arr, lo, hi, pivot):
    """Dutch National Flag partition. Returns (lt, gt) indices."""
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1; i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def my_sort(xs):
    """Return a new ascending-sorted list that is a permutation of *xs*."""
    n = len(xs)
    if n <= 1:
        return list(xs)

    # Work on a copy so the input is not mutated.
    arr = xs[:]
    _quicksort(arr, 0, n - 1)
    return arr


def _quicksort(arr, lo, hi):
    """In-place quicksort with median-of-three pivot and three-way partition."""
    while lo < hi:
        # Switch to insertion sort for small subarrays.
        if hi - lo <= 20:
            _insort(arr, lo, hi)
            break

        # Median-of-three pivot selection (first, middle, last).
        mid = (lo + hi) // 2
        a = arr[lo]; b = arr[mid]; c = arr[hi]
        if a > b:
            a, b = b, a
        if b > c:
            pivot = c
            lo += 1; hi -= 1
        elif a < b:
            pivot = a
            lo += 1; hi -= 1
        else:
            pivot = b

        # Three-way partition around *pivot*.
        lt, gt = _three_way_partition(arr, lo, hi, pivot)

        # Recurse on smaller half first (tail-call optimization).
        if lt - lo < hi - gt:
            _quicksort(arr, lo, lt - 1)
            lo = gt + 1
        else:
            _quicksort(arr, gt + 1, hi)
