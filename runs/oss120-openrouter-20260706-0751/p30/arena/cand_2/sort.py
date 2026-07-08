"""sort.py

Provides a single public function ``my_sort`` that returns a new list containing the
elements of *xs* sorted in ascending order.

The implementation deliberately uses only the Python standard library and relies on
the highly‑optimised Timsort algorithm behind :func:`sorted`.  This guarantees:

* **Correctness** – works for empty lists, single‑element lists, lists with duplicate
  values, negative numbers, and arbitrarily large integers (Python ints have
  unlimited precision).
* **Stability** – equal elements preserve their relative order, which is useful
  when the input carries hidden metadata.
* **Performance** – ``sorted`` runs in ``O(n log n)`` worst‑case time and ``O(n)``
  auxiliary space, and is written in C, so it is fast even for very large arrays.

The function returns a *new* list; the original ``xs`` is left untouched.
"""

from __future__ import annotations
from typing import Iterable, List, TypeVar

T = TypeVar("T")

def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a new list containing the elements of *xs* sorted in ascending order.

    Parameters
    ----------
    xs: Iterable[T]
        Any iterable of orderable items (e.g., ``int``, ``float``, ``str``).  The
        iterable is consumed and a *new* ``list`` with the sorted values is
        returned.

    Returns
    -------
    List[T]
        A sorted copy of the input.

    Notes
    -----
    * The function is a thin wrapper around the built‑in :func:`sorted` to give a
      stable, well‑named API required by the test harness.
    * ``sorted`` raises ``TypeError`` if the elements cannot be compared with each
      other – this is consistent with Python's sorting semantics.
    """
    # ``list()`` ensures we always return a list, even if ``xs`` is already a list.
    # ``sorted`` creates a new list internally, so this extra ``list`` call is only
    # needed for type‑checking clarity.
    return list(sorted(xs))

__all__: list[str] = ["my_sort"]
