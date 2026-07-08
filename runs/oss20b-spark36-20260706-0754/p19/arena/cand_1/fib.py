"""
Fast Fibonacci computation using fast‑doubling (O(log n)).

The implementation is minimal, uses only the Python standard library and
relies on Python's arbitrary‑precision integers for exact arithmetic.

Examples
--------
>>> fib(0)
0
>>> fib(1)
1
>>> fib(10)
55
>>> fib(100)
354224848179261915075
"""

from __future__ import annotations

__all__ = ["fib"]


# Fast‑doubling algorithm implementation.
# The function returns a tuple (F(n), F(n+1)).
# Recurrence:
#   F(2k)   = F(k) * [2*F(k+1) – F(k)]
#   F(2k+1) = F(k+1)^2 + F(k)^2
#             and  F(n+1) = F(n) + F(n-1).
# These formulas allow calculation in O(log n) steps.

def _fib_pair(n: int) -> tuple[int, int]:
    """Return (F(n), F(n+1)). Works for non‑negative integer *n*."""
    if n == 0:
        return 0, 1
    a, b = _fib_pair(n >> 1)
    # a = F(k), b = F(k+1) where k = n//2
    c = a * ((b << 1) - a)          # F(2k)
    d = a * a + b * b              # F(2k+1)
    if n & 1:
        return d, c + d            # F(2k+1), F(2k+2)
    else:
        return c, d                # F(2k),   F(2k+1)


def fib(n: int) -> int:
    """Return the *n*‑th Fibonacci number.

    Parameters
    ----------
    n : int
        Non‑negative integer index.  ``fib(0)`` returns ``0``, ``fib(1)``
        returns ``1``.

    Returns
    -------
    int
        The exact Fibonacci number F(n).

    Raises
    ------
    ValueError
        If *n* is negative.
    """
    if n < 0:
        raise ValueError("n must be non‑negative")
    return _fib_pair(n)[0]


if __name__ == "__main__":  # pragma: no cover
    import sys

    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("Usage: python fib.py <non‑negative integer>")
            sys.exit(1)
        print(fib(n))
    else:
        import doctest
        doctest.testmod()
"