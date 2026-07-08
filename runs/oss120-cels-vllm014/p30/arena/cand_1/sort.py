"""sort.py
~~~~~~~~~~~~~~~~
A tiny module exposing :func:`my_sort` – a drop‑in replacement for ``sorted`` that
returns a **new** list containing the elements of the input iterable in ascending
order.

Why not just use ``sorted``?
----------------------------
* The exercise explicitly asks for a function named ``my_sort``.
* We still want the best performance available in the standard library, so we
  delegate the heavy lifting to Python’s built‑in ``sorted`` which implements
  Timsort – a hybrid stable sort with O(n log n) worst‑case and O(n) best‑case
  (already sorted) behaviour.
* The implementation also demonstrates care for edge‑cases (empty input, single
  element, duplicate values, negative numbers, arbitrarily large integers) by
  simply forwarding the input to ``sorted`` – which already handles all of those
  correctly.

The function is deliberately tiny and well documented so that it can be used in
unit‑tests or as a reference implementation.
"""

from __future__ import annotations

from typing import Iterable, List, TypeVar

T = TypeVar("T")


def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a **new** list containing the items of *xs* in ascending order.

    Parameters
    ----------
    xs:
        Any iterable yielding orderable items (i.e. items that support the
        ``<`` comparison operator). The function does **not** modify *xs*.

    Returns
    -------
    list[T]
        A freshly allocated list sorted in non‑decreasing order.

    Edge‑case handling
    ------------------
    * **Empty input** – returns an empty list ``[]``.
    * **Singleton** – returns a one‑element list containing the same element.
    * **Duplicates** – all occurrences are retained; the multiset of elements
      is preserved.
    * **Negatives / big integers** – the built‑in ``sorted`` works with Python's
      arbitrary‑precision ``int`` type and with negative numbers without any
      special code.

    Performance
    ------------
    The function delegates to ``sorted`` which implements Timsort.  Timsort is
    stable, runs in O(n log n) worst‑case time and O(n) auxiliary space, and
    detects runs already in order to achieve O(n) time on nearly‑sorted data.
    For typical large arrays this is the fastest sorting algorithm available in
    the Python standard library.
    """
    # ``sorted`` returns a list; we simply forward the iterable.
    return sorted(xs)
