# fib.py
"""Fast Fibonacci using the fast‑doubling method.

Provides a single function ``fib(n)`` that returns the *exact* n‑th Fibonacci
number with ``fib(0) == 0`` and ``fib(1) == 1``.  The implementation runs in
O(log n) time and uses only Python's standard library and its built‑in arbitrary
precision integers.

The algorithm is based on the identities:
    F(2k)   = F(k) * (2*F(k+1) – F(k))
    F(2k+1) = F(k+1)^2 + F(k)^2
These allow us to compute ``(F(n), F(n+1))`` recursively in logarithmic depth.
"""

from __future__ import annotations
from typing import Tuple

def _fib_pair(n: int) -> Tuple[int, int]:
    """Return a tuple ``(F(n), F(n+1))`` using fast doubling.

    The function is defined for non‑negative ``n``.  It is implemented
    recursively; the recursion depth is at most ``log2(n)``.
    """
    if n == 0:
        return (0, 1)
    # Recursively compute F(k) and F(k+1) where k = n // 2
    a, b = _fib_pair(n >> 1)
    c = a * ((b << 1) - a)          # F(2k) = F(k) * (2*F(k+1) – F(k))
    d = a * a + b * b               # F(2k+1) = F(k)^2 + F(k+1)^2
    if n & 1:
        # n is odd --> return (F(2k+1), F(2k+2))
        return (d, c + d)
    else:
        # n is even --> return (F(2k), F(2k+1))
        return (c, d)


def fib(n: int) -> int:
    """Return the n‑th Fibonacci number.

    Parameters
    ----------
    n: int
        A non‑negative integer.  ``fib(0)`` returns ``0`` and ``fib(1)``
        returns ``1``.

    Raises
    ------
    ValueError
        If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    return _fib_pair(n)[0]


# Simple sanity check when the module is executed directly.
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fib.py <non‑negative integer>")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Argument must be an integer")
        sys.exit(1)
    print(fib(n))
