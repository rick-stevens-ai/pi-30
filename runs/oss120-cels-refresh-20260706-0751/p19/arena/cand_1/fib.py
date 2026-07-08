# fib.py
"""Fast Fibonacci using the fast‑doubling method.

Provides a single public function ``fib(n)`` returning the *n*‑th Fibonacci
number with ``fib(0) == 0`` and ``fib(1) == 1``.  The implementation runs in
``O(log n)`` time and uses only Python's built‑in arbitrary‑precision integers
(no external libraries).

The algorithm is based on the identities:

* ``F(2k)   = F(k) * (2*F(k+1) – F(k))``
* ``F(2k+1) = F(k)^2 + F(k+1)^2``

These allow us to halve the index at each recursive step (fast‑doubling).
"""

from __future__ import annotations

__all__ = ["fib"]


def _fib_pair(n: int) -> tuple[int, int]:
    """Return ``(F(n), F(n+1))`` using fast‑doubling.

    The function is tail‑recursive in the mathematical sense; the recursion
    depth is ``O(log n)`` which is safe for the large values required (e.g.
    ``n = 200_000``).
    """
    if n == 0:
        return 0, 1
    # Recursively obtain (F(k), F(k+1)) where k = n // 2
    a, b = _fib_pair(n >> 1)
    # Apply the doubling formulas
    c = a * ((b << 1) - a)          # F(2k)
    d = a * a + b * b                # F(2k+1)
    if n & 1:
        # n is odd -> return (F(2k+1), F(2k+2))
        return d, c + d
    else:
        # n is even -> return (F(2k), F(2k+1))
        return c, d


def fib(n: int) -> int:
    """Return the *n*‑th Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative index of the desired Fibonacci number.

    Returns
    -------
    int
        ``F(n)`` where ``F(0) == 0`` and ``F(1) == 1``.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non‑negative")
    return _fib_pair(n)[0]


if __name__ == "__main__":
    # Simple sanity check when run as a script.
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fib.py <non‑negative integer>")
        sys.exit(1)
    try:
        idx = int(sys.argv[1])
    except ValueError:
        print("Argument must be an integer.")
        sys.exit(1)
    print(fib(idx))
