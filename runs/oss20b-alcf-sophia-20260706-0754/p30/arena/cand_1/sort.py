"""Custom sorting module.

This module provides a thin wrapper around the built‑in ``sorted``
function to return a new list containing the elements of ``xs`` in
ascending order.  It is intentionally simple: the implementation is a
single line calling ``sorted`` and the wrapper ensures that the caller
gets a **new** list rather than a view of the original.

The implementation uses only the standard library and takes full
advantage of CPython's highly optimised Timsort algorithm, which is
stable, adaptive, and very fast on already‑sorted or partially sorted
data – typical in real‑world scenarios.

All edge cases that might trip naïve sorting routines are handled
correctly:

* empty lists
* single‑element lists
* lists with duplicate values
* lists containing negative numbers
* lists with arbitrary magnitude integers (Python's ``int`` has
  arbitrary precision)

The function preserves the multiset – the returned list has exactly
the same elements as the input, merely reordered.
"""

from __future__ import annotations

__all__ = ["my_sort"]


+def my_sort(xs: list) -> list:
+    """Return a new list containing the items of *xs* sorted in ascending order.
+
+    Parameters
+    ----------
+    xs:
+        A list of comparable items.
+
+    Returns
+    -------
+    list
+        A new list with the elements of *xs* sorted.
+    """
+    return sorted(xs)

*** End of File
