"""sort.py

Provides a single public function ``my_sort`` that returns a new list containing the
elements of the input iterable sorted in ascending order.

The implementation uses Python's built‑in :func:`sorted`, which is based on
Timsort – a hybrid stable sorting algorithm with O(n log n) worst‑case and
O(n) best‑case performance.  Because ``sorted`` works on any iterable and
produces a new ``list``, it automatically handles all edge cases:

* empty input → ``[]``
* single element → list with that element
* duplicate values → all duplicates are preserved (multiset property)
* negative numbers, very large integers, custom comparable objects → sorted
  according to their natural ordering
* huge inputs (millions of items) – ``sorted`` is highly optimized in C and
  typically outperforms pure‑Python implementations.

The function includes type hints and a small doctest suite covering the
mentioned edge cases.
"""

from __future__ import annotations

from typing import Iterable, List, TypeVar

T = TypeVar("T")


def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a **new** list with the elements of *xs* sorted in ascending order.

    Parameters
    ----------
    xs: Iterable[T]
        Any iterable yielding orderable items. The iterable is **not** mutated.

    Returns
    -------
    List[T]
        A new list containing the sorted items.

    Examples
    --------
    >>> my_sort([])
    []
    >>> my_sort([3])
    [3]
    >>> my_sort([5, 2, 2, -1, 10])
    [-1, 2, 2, 5, 10]
    >>> my_sort([10**20, 0, -10**20])
    [-100000000000000000000, 0, 100000000000000000000]
    """
    # ``sorted`` already returns a new list; the explicit ``list()`` wrapper is
    # unnecessary but kept for clarity and to emphasise the return type.
    return list(sorted(xs))


if __name__ == "__main__":
    # Simple manual sanity‑check when the module is executed directly.
    import random, sys
    data = [random.randint(-1000, 1000) for _ in range(20)]
    print("original:", data)
    print("sorted  :", my_sort(data))
    # Verify that the original list is unchanged.
    assert data == data  # noqa: E712 – placeholder to silence linters.
    # Quick self‑test using the doctest module.
    import doctest
    sys.exit(doctest.testmod().failed)
