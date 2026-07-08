"""Efficient Fibonacci implementation using fast doubling.

The module provides a single function :func:`fib` which returns the n-th
Fibonacci number (``fib(0) == 0`` and ``fib(1) == 1``).  The algorithm works in
O(log n) time and uses only integer arithmetic – Python's unlimited-precision
integers ensure that large results are represented exactly.

The implementation follows the classic fast‑doubling recurrence:

``F(2k)   = F(k) * (2*F(k+1) - F(k))``
``F(2k+1) = F(k+1)^2 + F(k)^2``

The helper :func:`_fib_pair` returns the pair ``(F(n), F(n+1))``.  The
recursion depth is ``O(log n)`` (≈ 18 for ``n = 200000``), so it is safe for
all non‑negative integer inputs.
"""

from __future__ import annotations

__all__ = ["fib"]


+def fib(n: int) -> int:
+    """Return the *n*-th Fibonacci number.
+
+    Parameters
+    ----------
+    n: int
+        Non‑negative integer index.
+
+    Returns
+    -------
+    int
+        The value of ``F(n)``.
+
+    Raises
+    ------
+    ValueError
+        If ``n`` is negative.
+    """
+    if not isinstance(n, int):
+        raise TypeError("n must be an integer")
+    if n < 0:
+        raise ValueError("n must be non‑negative")
+
+    def _fib_pair(k: int) -> tuple[int, int]:
+        """Return (F(k), F(k+1)).  Recursive helper for fast doubling.
+        """
+        if k == 0:
+            return (0, 1)
+        a, b = _fib_pair(k >> 1)  # a = F(k//2), b = F(k//2 + 1)
+        c = a * ((b << 1) - a)    # F(2*m)
+        d = a * a + b * b         # F(2*m+1)
+        if k & 1:
+            return (d, c + d)
+        else:
+            return (c, d)
+
+    return _fib_pair(n)[0]
+
*** End ***""