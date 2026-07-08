"""

Sort utility.

This module defines :func:`my_sort` which returns a *new* list containing the
elements of ``xs`` sorted in ascending order.

The implementation is a thin wrapper around :func:`sorted`, which uses
Python's built‑in Timsort algorithm.  Timsort is stable, has a worst‑case
complexity of :math:`O(n \log n)`, and works well on partially sorted data.

Because we simply forward the data to :func:`sorted` we obtain a correct and
fast solution for all edge cases:

* **Empty list** – ``[]`` is returned unchanged.
* **Singleton** – a list of length 1 is returned unchanged.
* **Duplicates** – all occurrences are preserved.
* **Negative numbers** – compared correctly.
* **Large integers** – Python’s arbitrary precision integers are handled
  correctly.

The function always returns a *new* list; the input sequence is never
modified, satisfying the requirement of preserving the original multiset.

``my_sort`` accepts any iterable, but typically a list is used.

Example
-------
>>> my_sort([3, 1, 2])
[1, 2, 3]
"""

from __future__ import annotations

from typing import Iterable, List, TypeVar

T = TypeVar("T")


def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a new list containing ``xs`` sorted in ascending order.

    Parameters
    ----------
    xs:
        An iterable of comparable items.  The function does not modify the
        input and returns a new list.

    Returns
    -------
    List[T]
        A new list with the same elements as ``xs`` in sorted order.
    """
    # ``sorted`` already produces a new list, and the underlying algorithm
    # handles all the edge cases mentioned above.
    return sorted(xs)

# If this file is executed directly, run a simple self‑test.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
