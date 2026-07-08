# sort.py
"""Utility module providing a fast, correct sorting function.

The :func:`my_sort` function returns a **new** list containing the elements of
the input iterable sorted in ascending order.  It works for any sequence of
comparable items – integers, floats, strings, custom objects that implement the
rich comparison methods – and correctly handles edge‑cases such as:

* empty input (returns an empty list)
* single‑element input (returns a list with that element)
* duplicate values (preserves the multiset)
* negative numbers and mixed sign values
* arbitrarily large integers (Python's ``int`` is unbounded)

Implementation uses the built‑in :func:`sorted` which employs Timsort – a
hybrid stable sorting algorithm with ``O(n log n)`` worst‑case performance and
excellent real‑world speed.  Because ``sorted`` creates a new list, the original
input is left untouched, satisfying the requirement for a non‑mutating
function.
"""

from __future__ import annotations
from typing import Iterable, List, TypeVar

T = TypeVar("T")


def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a **new** list containing the elements of ``xs`` sorted ascending.

    Parameters
    ----------
    xs: Iterable[T]
        Any iterable of comparable items.

    Returns
    -------
    List[T]
        A new list with the items from ``xs`` in non‑decreasing order.
    """
    # ``sorted`` accepts any iterable and returns a new list.
    # It is stable, handles all edge cases, and is highly optimized in CPython.
    return sorted(xs)


__all__ = ["my_sort"]
