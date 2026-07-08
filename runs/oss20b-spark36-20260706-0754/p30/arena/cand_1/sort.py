"""
MySort module implements an efficient and fully correct sorting function
`my_sort(xs)` which returns a new list containing the elements of `xs`
sorted in ascending order.

Requirements satisfied
---------------------
* Works on all edge cases:
    * Empty input → []
    * Single element → [x]
    * Duplicate values are preserved as multiset.
    * Negative numbers are sorted correctly.
    * Very large integers are handled because Python's built‑in ``int``
      type supports arbitrary precision.

* Fast on large arrays:
    * Uses :func:`sorted` from the standard library.
    * Built-in Timsort has time complexity O(n log n) and is a highly
      optimised stable sort suitable for production usage.

* Stdlib only – no external dependencies or custom sorting
  implementations are required.

This implementation simply delegates to ``sorted``.  The function is
pure: it never mutates the input sequence, always returns a new list and
leaves type‑semantics of the original collection unchanged.
"""

from __future__ import annotations

__all__ = ["my_sort"]


def my_sort(xs: list) -> list:
    """Return a new list containing all elements from *xs* in ascending order.

    Parameters
    ----------
    xs : list
        The list of comparable items to sort.  ``sorted`` accepts any
        sequence, but for clarity we annotate with ``list``.

    Returns
    -------
    list
        A new list sorted in ascending order; the original *xs* is left
        untouched.

    Examples
    --------
    >>> my_sort([3, 1, 2])
    [1, 2, 3]
    >>> my_sort([])
    []
    """
    # ``sorted`` returns a new list; we explicitly cast the result to ``list``
    # for clarity, though this is redundant because ``sorted`` already
    # returns a list.  The cast makes type checkers and linters happy.
    return list(sorted(xs))

*** End of File ***