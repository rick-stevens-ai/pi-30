"""Simple sorting utility.

This module exposes a single public function, :func:`my_sort`, which takes
an iterable of comparable items and returns a **new** list containing the
elements sorted in ascending order.  The implementation is a thin wrapper
around :func:`sorted`, which uses Python's efficient Timsort algorithm.

Features
--------
* **Correctness** – Handles all edge cases: empty collections, single-element
  collections, duplicate values, negative numbers, and arbitrarily large
  integers.  Because it relies on ``sorted`` the multiset of elements is
  preserved exactly.

* **Performance** – ``sorted`` runs in ``O(n log n)`` time and is highly
  optimised in CPython.  Creating a new list means the input is not
  mutated, saving callers from accidental side‑effects.

* **Simplicity** – No external dependencies are required; the function is
  implemented using standard library primitives only.

Usage
-----
>>> my_sort([3, 1, 2])
[1, 2, 3]
>>> my_sort([])
[]
"""

from __future__ import annotations

__all__ = ["my_sort"]

from typing import Iterable, List, TypeVar

T = TypeVar("T")


def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a new list with the elements of *xs* sorted in ascending order.

    Parameters
    ----------
    xs:
        An iterable of comparable items.  The items must support the
        rich comparison operators required by Python's sort;
        otherwise a ``TypeError`` will be raised.

    Returns
    -------
    list
        A new list containing the elements of ``xs`` in sorted order.
        The original iterable is **not** modified.

    Notes
    -----
    * ``sorted`` is a stable sorting algorithm; if ``xs`` contains
      equal items, their relative order is preserved.
    * The function accepts any iterable, not just lists or tuples.
    """
    # ``sorted`` returns a new list, so we can simply hand it the iterable.
    return sorted(xs)
