# fib.py
"""Fast Fibonacci using fast‑doubling (O(log n)).

The module provides a single public function:

    fib(n) -> int

where ``fib(0) == 0`` and ``fib(1) == 1``.  The implementation works with
arbitrary‑size integers (Python's built‑in ``int``) and is efficient enough to
compute ``fib(200_000)`` in well under a second.

The algorithm is based on the identities:

    F(2k)   = F(k) * (2*F(k+1) – F(k))
    F(2k+1) = F(k+1)^2 + F(k)^2

These allow us to compute ``(F(n), F(n+1))`` recursively, halving the index at
each step, yielding a logarithmic runtime.
"""

from __future__ import annotations
from typing import Tuple

__all__ = ["fib"]


def _fib_pair(n: int) -> Tuple[int, int]:
    """Return ``(F(n), F(n+1))`` using fast‑doubling.

    The function is defined for non‑negative ``n``; callers should validate the
    input beforehand.  The recursion depth is at most ``log2(n)``.
    """
    if n == 0:
        return 0, 1
    # Recursively compute (F(k), F(k+1)) where k = n // 2
    a, b = _fib_pair(n >> 1)
    # Apply the doubling formulas
    c = a * ((b << 1) - a)          # F(2k)
    d = a * a + b * b               # F(2k+1)
    if n & 1:
        # n is odd -> return (F(2k+1), F(2k+2))
        return d, c + d
    else:
        # n is even -> return (F(2k), F(2k+1))
        return c, d


def fib(n: int) -> int:
    """Return the *n*th Fibonacci number (0‑based).

    Parameters
    ----------
    n: int
        Non‑negative integer index.

    Returns
    -------
    int
        ``F(n)`` where ``F(0) = 0`` and ``F(1) = 1``.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    return _fib_pair(n)[0]

# Simple sanity test when the module is executed directly.
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fib.py <non‑negative integer>")
        sys.exit(1)
    try:
        index = int(sys.argv[1])
    except ValueError:
        print("Argument must be an integer.")
        sys.exit(1)
    print(fib(index))
