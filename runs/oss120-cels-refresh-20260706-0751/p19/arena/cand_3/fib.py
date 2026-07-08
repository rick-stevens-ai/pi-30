# fib.py
"""Fast Fibonacci calculation using the fast‑doubling method.

Provides a single public function ``fib`` that returns the *n*th Fibonacci
number (with ``fib(0) == 0`` and ``fib(1) == 1``).  The implementation works
with Python's unlimited‑precision ``int`` and runs in ``O(log n)`` time, so
calculating ``fib(200_000)`` completes in well under a second.

Only the Python standard library is used.
"""

__all__ = ["fib"]


def _fib_pair(n: int) -> tuple[int, int]:
    """Return ``(F(n), F(n + 1))`` using fast‑doubling recursion.

    The algorithm is based on the identities:
        F(2k)   = F(k)·[2·F(k+1) – F(k)]
        F(2k+1) = F(k)^2 + F(k+1)^2
    It runs in ``O(log n)`` because each recursive call halves ``n``.
    """
    if n == 0:
        return (0, 1)
    # Recursively compute F(k) and F(k+1) where k = n // 2
    a, b = _fib_pair(n >> 1)
    # Apply the doubling formulas
    c = a * ((b << 1) - a)   # F(2k)
    d = a * a + b * b        # F(2k+1)
    if n & 1:
        # n is odd → return (F(2k+1), F(2k) + F(2k+1))
        return (d, c + d)
    else:
        # n is even → return (F(2k), F(2k+1))
        return (c, d)


def fib(n: int) -> int:
    """Return the *n*th Fibonacci number.

    Parameters
    ----------
    n: int
        The index of the Fibonacci number to compute. ``n`` must be a
        non‑negative integer.

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
