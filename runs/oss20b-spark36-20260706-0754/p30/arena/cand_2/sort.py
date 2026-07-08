"""Utility module providing a `my_sort` function.

The implementation uses the built‑in :func:`sorted` which is based on Timsort –
an adaptive, stable sort that is fast (O(n log n)) even for large arrays and
handles all edge cases out of the box.  No external dependencies are used; all
functionality comes from the Python standard library.

The module exposes only one public name via ``__all__``.
"""

from typing import Iterable, List, TypeVar

T = TypeVar("T")

__all__ = ["my_sort"]


def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a **new** list containing the elements of *xs* sorted in
    ascending order.

    Parameters
    ----------
    xs:
        An iterable yielding comparable items.  The function does not modify
        *xs*; it always produces a fresh list.

    Returns
    -------
    List[T]
        A new list with the sorted elements.

    Notes
    -----
    - The implementation relies on :func:`sorted`, which is stable and
      preserves duplicate items, handling ``None`` (if comparable), negative
      numbers, large integers, empty iterables, etc., correctly.
    """
    # Convert the iterable to a list via sorted – this produces a new list
    # with O(n log n) complexity using Timsort.  Using a generator
    # comprehension keeps the memory footprint minimal for non‑list
    # iterables.
    return sorted(xs)

