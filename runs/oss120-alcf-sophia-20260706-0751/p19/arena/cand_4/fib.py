# fib.py
"""Fast‑doubling Fibonacci implementation.

Provides a single public function ``fib(n)`` that returns the *n*‑th Fibonacci
number with ``fib(0) == 0`` and ``fib(1) == 1``.

The algorithm runs in ``O(log n)`` time using the *fast‑doubling* identities:

* ``F(2k)   = F(k) * (2*F(k+1) – F(k))``
* ``F(2k+1) = F(k+1)^2 + F(k)^2``

Both identities are derived from matrix exponentiation and avoid the linear
cost of the naïve recursion or the ``O(n)`` iterative approach.  Python's
arbitrary‑precision integers (bigints) handle the large values required for
``n = 200_000`` without overflow.

Only the Python standard library is used.
"""

from __future__ import annotations
from typing import Tuple

def _fib_pair(n: int) -> Tuple[int, int]:
    """Return ``(F(n), F(n+1))`` using fast‑doubling.

    The function is written recursively; the recursion depth is at most
    ``log2(n)`` (≈ 18 for ``n = 200_000``), well within Python's default limit.
    """
    if n == 0:
        return (0, 1)
    # Recurse on n // 2
    a, b = _fib_pair(n >> 1)
    # Apply doubling formulas
    c = a * ((b << 1) - a)          # F(2k)   = F(k) * (2*F(k+1) – F(k))
    d = a * a + b * b               # F(2k+1) = F(k)^2 + F(k+1)^2
    if n & 1:
        # n is odd -> return (F(2k+1), F(2k+2))
        return (d, c + d)
    else:
        # n is even -> return (F(2k), F(2k+1))
        return (c, d)


def fib(n: int) -> int:
    """Return the *n*‑th Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative integer index.  ``fib(0)`` returns ``0`` and ``fib(1)``
        returns ``1``.

    Raises
    ------
    ValueError
        If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    return _fib_pair(n)[0]


# Simple sanity checks when run as a script
if __name__ == "__main__":
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    except ValueError:
        print("Please provide a non‑negative integer argument.")
        sys.exit(1)
    print(f"fib({n}) = {fib(n)}")
    # Quick verification for a few known values
    known = {0: 0, 1: 1, 2: 1, 3: 2, 10: 55, 20: 6765}
    for k, v in known.items():
        assert fib(k) == v, f"Incorrect result for fib({k})"
    print("All sanity checks passed.")
