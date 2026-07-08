'''sort.py

Utility module exposing a single function ``my_sort`` which returns a new sorted list.

The implementation relies on Python's built‑in :func:`sorted`, which uses the highly
optimized Timsort algorithm (O(n log n) worst‑case, O(n) best‑case for already sorted
data).  This guarantees correct ordering for all edge cases:

* Empty input → ``[]``
* Single element → ``[elem]``
* Duplicates → all copies are retained and appear consecutively
* Negative numbers and arbitrarily large integers are handled because comparison
  of ``int`` objects in Python is exact and unbounded.
* The original iterable is never modified – a brand new list is returned.

Only the Python standard library is used.
''' 

from __future__ import annotations

from typing import Iterable, List, TypeVar

T = TypeVar("T")

__all__ = ["my_sort"]


def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a **new** list containing the elements of *xs* sorted in ascending order.

    Parameters
    ----------
    xs: Iterable[T]
        Any iterable of comparable items. The items must support the ``<`` operator.

    Returns
    -------
    List[T]
        A new list with the same multiset of elements as *xs*, ordered from the
        smallest to the largest value.

    Notes
    -----
    * The function does **not** modify the input.
    * ``sorted`` raises ``TypeError`` if the elements are not mutually comparable;
      this behaviour is propagated unchanged.
    * For large inputs the underlying Timsort implementation is fast and memory‑
      efficient (it works in‑place on a temporary list and then returns it).
    """
    # ``sorted`` creates a new list, guaranteeing we never mutate the original.
    return sorted(xs)
