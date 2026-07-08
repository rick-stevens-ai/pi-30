"""sort.py

Defines :func:`my_sort` which returns a new sorted list in ascending order.

This implementation is intentionally lightweight: it delegates the heavy lifting
to Python's built‑in :func:`sorted`, which uses the highly efficient Timsort
algorithm.  It is correct for all edge cases – empty lists, singletons,
duplicates, negative numbers, very large integers – and guarantees that the
returned list is a *new* list, leaving the input list unmodified.

Because :func:`sorted` operates in O(n log n) time and is stable, it is
appropriate for large arrays while also preserving the multiset of the
original list.

Example
-------
>>> my_sort([3, 1, 2])
[1, 2, 3]
"""

from typing import List, Sequence, TypeVar

T = TypeVar("T")

__all__ = ["my_sort"]


def my_sort(xs: Sequence[T]) -> List[T]:
    """Return a new list with the elements of *xs* sorted ascending.

    Parameters
    ----------
    xs : Sequence[T]
        Any sequence of elements that support comparison operators.

    Returns
    -------
    List[T]
        A new list containing all items from *xs* in ascending order.

    Notes
    -----
    * The input sequence is **not** modified.
    * The function works with any orderable type: numbers, strings,
      custom objects with ``__lt__``/``__gt__`` defined, etc.
    * ``sorted`` uses Timsort (a hybrid stable sorting algorithm derived
      from merge sort and insertion sort), making this implementation
      both fast and stable.
    """
    return sorted(xs)

*** End of file ***
