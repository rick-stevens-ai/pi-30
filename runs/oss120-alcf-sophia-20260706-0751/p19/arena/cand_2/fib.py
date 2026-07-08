# fib.py
"""Fast Fibonacci using fast‑doubling (O(log n)).

Provides:
    fib(n) -> int
        Returns the nth Fibonacci number (0‑indexed, F(0)=0, F(1)=1).

The implementation uses only the Python standard library and works with
arbitrary‑size integers (Python's built‑in ``int`` type).
"""

from __future__ import annotations
from typing import Tuple

__all__ = ["fib"]


def _fib_pair(n: int) -> Tuple[int, int]:
    """Return (F(n), F(n+1)) using the fast‑doubling recurrence.

    The algorithm is described in many textbooks and runs in O(log n) time.
    It works for any non‑negative integer ``n``.
    """
    if n == 0:
        return (0, 1)
    # Recursively compute half‑pair
    a, b = _fib_pair(n >> 1)
    # c = F(2k)   = F(k) * (2*F(k+1) – F(k))
    c = a * ((b << 1) - a)
    # d = F(2k+1) = F(k)^2 + F(k+1)^2
    d = a * a + b * b
    if n & 1:
        # n is odd: return (F(2k+1), F(2k+2)) = (d, c + d)
        return (d, c + d)
    else:
        # n is even: return (F(2k), F(2k+1)) = (c, d)
        return (c, d)


def fib(n: int) -> int:
    """Return the nth Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative index of the Fibonacci sequence.

    Returns
    -------
    int
        The nth Fibonacci number.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    return _fib_pair(n)[0]


if __name__ == "__main__":
    # Simple sanity checks when run as a script
    import sys
    if len(sys.argv) > 1:
        try:
            value = int(sys.argv[1])
        except ValueError:
            sys.exit("Argument must be an integer")
        print(fib(value))
    else:
        # Demo for a few values
        for i in range(10):
            print(i, fib(i))
