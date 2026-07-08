# sort.py
"""A simple, fast, and correct sorting utility.

Provides :func:`my_sort` which returns a new list containing the elements of the
input iterable sorted in ascending order.

Features
--------
* Works with any iterable that yields orderable items (ints, floats, strings,
  custom objects implementing ``__lt__``).
* Handles edge‑cases gracefully – empty iterables, single‑element iterables,
  duplicate values, negative numbers and arbitrarily large integers.
* Returns a **new** list; the original input is never mutated.
* Leverages Python's built‑in ``sorted`` which implements TimSort – a stable,
  adaptive, O(n log n) algorithm that is optimised for real‑world data.
* Only the standard library is used.
"""

from __future__ import annotations

from typing import Iterable, List, TypeVar

_T = TypeVar("_T")

__all__ = ["my_sort"]


def my_sort(xs: Iterable[_T]) -> List[_T]:
    """Return a **new** list with the elements of *xs* sorted in ascending order.

    Parameters
    ----------
    xs:
        An iterable of orderable items. The function does **not** require the
        argument to be a list – any iterable (generator, tuple, etc.) is
        acceptable.

    Returns
    -------
    list
        A freshly allocated list containing the sorted elements.

    Notes
    -----
    * The implementation simply forwards to :func:`sorted`, which uses the
      highly‑optimised TimSort algorithm (stable, O(n log n) worst‑case, O(n)
      best‑case for already‑sorted data).
    * Because a new list is created, the original ``xs`` is left untouched –
      this satisfies the requirement to preserve the input multiset without
      side‑effects.
    * For very large inputs (tens of millions of items) the function remains
      memory‑efficient as it only stores the resulting list and the temporary
      structures required by ``sorted``.
    """
    # ``sorted`` returns a new list, guaranteeing the required behaviour.
    return sorted(xs)

# Simple sanity‑check when the module is executed directly.
if __name__ == "__main__":
    # Demonstration of edge‑cases
    test_cases = [
        [],
        [42],
        [3, 1, 2, 1, 3],
        [-5, -2, -9, 0, 7],
        [10**20, 10**10, 10**30],
    ]
    for case in test_cases:
        print(f"input: {case!r} -> sorted: {my_sort(case)!r}")
