# sort.py
"""
A drop-in replacement for :func:`sorted` that returns a new list sorted in
ascending order.

The implementation is a classic *merge‑sort* which:

* works correctly for all edge‑cases – empty list, single element, duplicated
  values, negative numbers and arbitrarily large integers;
* preserves the input multiset (the output is a permutation of the input);
* runs in ``O(n log n)`` time and ``O(n)`` auxiliary space – comparable to the
  CPython ``list.sort`` implementation for the vast majority of realistic data
  sizes.

Only the Python standard library is used – no third‑party dependencies.

Typical usage::

    from sort import my_sort
    result = my_sort([3, 1, 2])  # -> [1, 2, 3]

The function never mutates the passed ``xs`` sequence; a brand‑new list is
always returned.
"""

from __future__ import annotations
from typing import List, Sequence, TypeVar

T = TypeVar("T")

def _merge(left: List[T], right: List[T]) -> List[T]:
    """Merge two *already* sorted lists and return a new sorted list.

    The algorithm walks both lists with two indices and appends the smaller
    element at each step.  Because we never modify the input lists we keep the
    function pure and safe for all caller‑provided data.
    """
    merged: List[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    # One of the lists may have leftovers – extend them unchanged.
    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])
    return merged

def _merge_sort(seq: List[T]) -> List[T]:
    """Recursively sort *seq* using merge‑sort.

    For tiny inputs (≤16 elements) insertion sort is used because it has lower
    constant overhead.  This hybrid approach yields a noticeable speed‑up on
    real‑world data while keeping the asymptotic guarantees of merge‑sort.
    """
    n = len(seq)
    if n <= 1:
        return seq[:]
    if n <= 16:  # insertion sort for very small arrays
        # Copy to avoid mutating the original list.
        arr = seq[:]
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    mid = n // 2
    left = _merge_sort(seq[:mid])
    right = _merge_sort(seq[mid:])
    return _merge(left, right)

def my_sort(xs: Sequence[T]) -> List[T]:
    """Return a **new** list containing the items from ``xs`` sorted ascending.

    The function accepts any :class:`collections.abc.Sequence` – for example a
    list, tuple or ``range`` – and always returns a fresh ``list`` instance.

    Edge‑case handling:

    * ``xs`` may be empty – an empty list is returned.
    * ``xs`` may contain duplicate values – the multiplicity is preserved.
    * ``xs`` may contain negative numbers or arbitrarily large integers – the
      comparison operators work unchanged because Python's ``int`` type has
      unbounded precision.
    """
    # Convert the input to a list *once* – this guarantees O(1) indexing for
    # the recursive algorithm and also decouples us from any mutable input.
    data = list(xs)
    return _merge_sort(data)

# ---------------------------------------------------------------------------
# Simple self‑test when the module is executed directly.  This is *not*
# a replacement for a proper test suite but provides a quick sanity check.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        [],
        [1],
        [2, 1],
        [3, 1, 2, 1, 5, -1, 0, 0],
        list(range(1000, 0, -1)),  # reverse‑sorted large list
    ]
    for case in test_cases:
        expected = sorted(case)
        result = my_sort(case)
        assert result == expected, f"my_sort failed for {case}\ngot {result}\nexp {expected}"
    print("All quick sanity checks passed.")
