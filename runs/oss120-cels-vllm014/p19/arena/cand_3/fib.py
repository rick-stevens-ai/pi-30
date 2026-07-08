# fib.py
"""Fast Fibonacci using the fast‑doubling method.

Provides a single public function ``fib(n)`` that returns the *n*th Fibonacci
number with ``fib(0) == 0`` and ``fib(1) == 1``.  The implementation runs in
``O(log n)`` time and uses only the Python standard library; the result is a
native ``int`` (arbitrary‑precision bigint).

The algorithm follows the identities:

* ``F(2k)   = F(k) * (2*F(k+1) – F(k))``
* ``F(2k+1) = F(k+1)^2 + F(k)^2``

These allow us to compute ``F(n)`` recursively while halving ``n`` each step.
"""

from __future__ import annotations
from typing import Tuple

__all__ = ["fib"]


def _fib_pair(n: int) -> Tuple[int, int]:
    """Return ``(F(n), F(n+1))`` using fast‑doubling.

    The function is deliberately internal – callers should use :func:`fib`.
    It works for any non‑negative integer ``n`` and runs in ``O(log n)`` time.
    """
    if n == 0:
        return 0, 1
    # Recursively compute (F(k), F(k+1)) where k = n // 2
    a, b = _fib_pair(n >> 1)
    # Apply doubling formulas
    c = a * ((b << 1) - a)          # F(2k) = F(k) * (2*F(k+1) – F(k))
    d = a * a + b * b               # F(2k+1) = F(k)^2 + F(k+1)^2
    if n & 1:
        # n is odd -> return (F(2k+1), F(2k+2))
        return d, c + d
    else:
        # n is even -> return (F(2k), F(2k+1))
        return c, d


def fib(n: int) -> int:
    """Return the *n*th Fibonacci number.

    Parameters
    ----------
    n: int
        Index of the Fibonacci number (``n >= 0``).

    Returns
    -------
    int
        The exact ``n``th Fibonacci number.
    """
    if n < 0:
        raise ValueError("fib is not defined for negative indices")
    return _fib_pair(n)[0]


# Simple sanity check when the module is executed directly.
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fib.py <non‑negative integer>")
        sys.exit(1)
    try:
        idx = int(sys.argv[1])
    except ValueError:
        print("Argument must be an integer")
        sys.exit(1)
    print(fib(idx))
