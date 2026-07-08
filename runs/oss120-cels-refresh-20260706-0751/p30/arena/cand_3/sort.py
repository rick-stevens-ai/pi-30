"""sort.py

Provides a single function ``my_sort`` that returns a new list containing the
elements of the input iterable sorted in ascending order.

The implementation uses the ``heapq`` module (a binary heap) rather than the
built‑in ``sorted`` function, offering a distinct algorithmic angle while still
being fast (``O(n log n)``) and fully compliant with Python's comparison rules.

It correctly handles all edge cases:

* Empty input – returns ``[]``.
* Single‑element input – returns a list with that element.
* Duplicate values – all copies are preserved.
* Negative numbers and arbitrarily large integers – Python's comparisons work
  for any ``int`` size, and ``heapq`` respects the ordering.
* Any other comparable objects (e.g., ``float``, ``str``) are also supported.

Only the standard library is used.
"""

from __future__ import annotations

from typing import Iterable, List, TypeVar
import heapq

T = TypeVar("T")

__all__ = ["my_sort"]


def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a **new** list with the items of *xs* sorted in ascending order.

    The function works with any iterable whose items are mutually comparable.
    It builds a binary heap via :func:`heapq.heapify` and then repeatedly pops
    the smallest element, yielding an ``O(n log n)`` time complexity and
    ``O(n)`` additional memory for the output list.

    Parameters
    ----------
    xs:
        An iterable of comparable items.

    Returns
    -------
    List[T]
        A new list containing the sorted items.
    """
    # Convert the input to a list of (value, index, original_item) tuples.
    # The index ensures a stable ordering for elements that compare equal.
    # ``heapify`` will order first by the value, then by the index.
    enumerated: List[tuple[T, int, T]] = [(x, i, x) for i, x in enumerate(xs)]
    heapq.heapify(enumerated)
    # Pop items one‑by‑one; each popped tuple yields the original item in stable order.
    return [heapq.heappop(enumerated)[2] for _ in range(len(enumerated))]
