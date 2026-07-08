# fib.py
"""Efficient Fibonacci number calculation using fast doubling.

The module provides a single public function:

    fib(n) -> int

which returns the nth Fibonacci number with the convention:
    fib(0) == 0
    fib(1) == 1

The implementation runs in O(log n) time and uses only the Python
standard library, leveraging Python's arbitrary‑precision integers.
"""

from __future__ import annotations
from typing import Tuple

__all__ = ["fib"]


def _fib_pair(k: int) -> Tuple[int, int]:
    """Return (F(k), F(k+1)) using the fast‑doubling recurrence.

    The recurrence relations are::

        F(2m)   = F(m) * (2*F(m+1) – F(m))
        F(2m+1) = F(m+1)**2 + F(m)**2

    This helper is implemented recursively but the depth is at most
    ``log2(k)`` (≈ 18 for ``k = 200_000``), well within Python's recursion
    limits.
    """
    if k == 0:
        return 0, 1
    # Recursively compute (F(m), F(m+1)) where m = k // 2
    a, b = _fib_pair(k >> 1)
    # Apply the doubling formulas
    c = a * ((b << 1) - a)          # F(2m)
    d = a * a + b * b               # F(2m+1)
    if k & 1:
        # k is odd → return (F(2m+1), F(2m+2))
        return d, c + d
    else:
        # k is even → return (F(2m), F(2m+1))
        return c, d


def fib(n: int) -> int:
    """Return the *n*th Fibonacci number.

    Parameters
    ----------
    n: int
        A non‑negative integer.

    Returns
    -------
    int
        ``F(n)`` where ``F(0)=0`` and ``F(1)=1``.

    Raises
    ------
    ValueError
        If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    # ``_fib_pair`` returns (F(n), F(n+1)) – we only need the first value.
    return _fib_pair(n)[0]

# Simple sanity check when the module is executed directly.
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fib.py <non‑negative integer>")
        sys.exit(1)
    try:
        val = int(sys.argv[1])
    except ValueError:
        print("Argument must be an integer")
        sys.exit(1)
    print(fib(val))
