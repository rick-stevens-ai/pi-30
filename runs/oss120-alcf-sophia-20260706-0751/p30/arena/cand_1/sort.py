"""sort.py

Provides a single public function :func:`my_sort` that returns a new list
containing the elements of the input sequence sorted in ascending order.

The implementation relies on Python's built‑in :func:`sorted`, which uses the
highly‑optimized Timsort algorithm.  This guarantees:

* **Correctness** – works for all edge‑cases including empty sequences,
  single‑element sequences, duplicate values, negative numbers, and arbitrarily
  large integers.
* **Stability** – equal elements retain their original relative order, preserving
  the multiset semantics.
* **Performance** – Timsort runs in ``O(n log n)`` worst‑case time with very
  good real‑world constants, making it suitable for large arrays.

Only the standard library is used; no external dependencies.
"""

from __future__ import annotations

from typing import List, Sequence, TypeVar

T = TypeVar("T", bound="Comparable")

class Comparable:
    """A protocol for values that support the ``<`` comparison operator.

    The built‑in numeric types (int, float, Decimal, etc.) already satisfy this
    requirement, so the generic type ``T`` can be any of those without further
    constraints.
    """

    def __lt__(self, other: object) -> bool: ...  # pragma: no cover


def my_sort(xs: Sequence[T]) -> List[T]:
    """Return a new list containing the elements of *xs* sorted in ascending order.

    Parameters
    ----------
    xs: Sequence[T]
        The input collection. It may be a list, tuple, or any other sequence type.

    Returns
    -------
    List[T]
        A **new** list with the elements of ``xs`` sorted. The original ``xs`` is
        left untouched.
    """
    # ``sorted`` creates a new list and does not mutate the input.
    return list(sorted(xs))

__all__ = ["my_sort"]
