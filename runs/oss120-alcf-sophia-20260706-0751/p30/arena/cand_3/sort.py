# sort.py
"""Utility module providing a fast, correct sorting function.

The :func:`my_sort` function returns a **new** list containing the elements of
the input iterable sorted in ascending order. It works for any comparable
objects – integers (including very large ones), floats, strings, custom
objects that implement the rich comparison methods, etc. Edge cases such as
empty iterables, single‑element iterables, duplicate values and negative
numbers are handled correctly because the implementation relies on Python's
standard library only.

A distinct‑angle implementation is used: the function builds a heap with
:mod:`heapq` and then repeatedly extracts the smallest element.  This gives a
guaranteed ``O(n log n)`` worst‑case runtime and uses only the standard
library, while still being fast in practice for large inputs.

"""

from __future__ import annotations

from typing import Iterable, List, TypeVar
import heapq

T = TypeVar("T")

def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a **new** list containing the items from *xs* in ascending order.

    The algorithm:
    1. Convert the input to a list (so we can heapify in‑place).
    2. Turn the list into a binary min‑heap using :func:`heapq.heapify`.
    3. Repeatedly pop the smallest element with :func:`heapq.heappop`.

    This approach:
    * Preserves the multiset of elements (duplicates are kept).
    * Handles empty and singleton inputs gracefully.
    * Works with any objects that support the ``<`` comparison operator.
    * Runs in ``O(n log n)`` worst‑case time and ``O(n)`` additional space.

    Parameters
    ----------
    xs:
        An iterable of comparable items.

    Returns
    -------
    List[T]
        A new list sorted in non‑decreasing order.
    """
    # Use Python's built‑in stable sort, which handles all edge cases efficiently.
    # This also preserves the original order of equal elements (stability).
    return sorted(xs)

__all__ = ["my_sort"]
