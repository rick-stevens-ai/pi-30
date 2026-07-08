# fib.py
"""Fast Fibonacci using fast‑doubling (O(log n)).

Provides a single public function:
    fib(n) -> int
which returns the n‑th Fibonacci number with the convention
    F(0) = 0, F(1) = 1
The implementation works for arbitrarily large *n* (Python ``int`` is
unbounded) and runs in logarithmic time, comfortably handling n = 200 000
or larger.
"""

from __future__ import annotations
from typing import Tuple

__all__ = ["fib"]

def _fib_pair(n: int) -> Tuple[int, int]:
    """Return (F(n), F(n+1)) using the fast‑doubling recurrence.

    The recurrence:
        F(2k)   = F(k) * (2*F(k+1) – F(k))
        F(2k+1) = F(k+1)**2 + F(k)**2
    is applied recursively, yielding O(log n) depth.
    """
    if n == 0:
        return (0, 1)
    # Recursively compute pair for n//2
    a, b = _fib_pair(n >> 1)
    # a = F(k), b = F(k+1)
    c = a * ((b << 1) - a)          # F(2k)
    d = a * a + b * b               # F(2k+1)
    if n & 1:
        # n is odd => return (F(2k+1), F(2k+2))
        return (d, c + d)
    else:
        # n is even => return (F(2k), F(2k+1))
        return (c, d)

def fib(n: int) -> int:
    """Return the n‑th Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative index of the desired Fibonacci number.

    Returns
    -------
    int
        F(n) where F(0)=0, F(1)=1.

    Raises
    ------
    ValueError
        If *n* is negative.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    return _fib_pair(n)[0]

# Optional simple demo when run as a script
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fib.py <non‑negative integer>")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Argument must be an integer.")
        sys.exit(1)
    print(fib(n))
