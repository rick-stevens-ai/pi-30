"""Custom sorting implementation.

This module implements :func:`my_sort`, which returns a new list with the
elements of ``xs`` sorted in ascending order.  The implementation uses the
standard library :mod:`heapq` module. The financed algorithm has a
time complexity of :math:`O(n\log n)` and preserves the multiset of the
input: duplicates are kept, negative numbers are handled just as any
other values, and the original iterable is left untouched.

The function works correctly for all the common edge cases:

* Empty input –``[]`` is returned.
* Singleton input – the original value is returned in a single‑element list.
* Duplicate values – all occurrences are included in the result.
* Negative and very large integers – handled automatically.

``my_sort`` accepts any :class:`~collections.abc.Iterable` of objects that
support the ``<`` comparison operator. The returned list is freshly
allocated.
"""

from __future__ import annotations

import heapq
from typing import Iterable, List, TypeVar

T = TypeVar("T")
__all__ = ["my_sort"]


def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a new list containing all items from *xs* eliminatively sorted.

    Parameters
    ----------
    xs : Iterable[T]
        Any iterable of comparable items.

    Returns
    -------
    List[T]
        A list with the items in non‑decreasing order.
    """
    data: List[T] = list(xs)
    if not data:
        return []
    heapq.heapify(data)
    return [heapq.heappop(data) for _ in range(len(data))]
