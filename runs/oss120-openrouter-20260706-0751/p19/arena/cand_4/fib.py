"""fib.py

Fast Fibonacci calculation using the fast‑doubling method.

The function ``fib`` returns the *n*‑th Fibonacci number with the convention
``fib(0) == 0`` and ``fib(1) == 1``.  The implementation runs in
``O(log n)`` time and uses only the Python standard library, taking full
advantage of Python's arbitrary‑precision integers.

The algorithm is based on the identities:
    F(2k)   = F(k) * (2*F(k+1) – F(k))
    F(2k+1) = F(k+1)^2 + F(k)^2
These allow us to compute ``(F(n), F(n+1))`` recursively in logarithmic
depth.
"""

from __future__ import annotations
from typing import Tuple

__all__ = ["fib"]


def _fib_pair(n: int) -> Tuple[int, int]:
    """Return ``(F(n), F(n+1))`` using fast doubling.

    The function works for non‑negative integers ``n``.  It is implemented
    recursively; the recursion depth is at most ``log2(n)`` which is safe for
    the required range (e.g., ``n = 200_000``).
    """
    if n == 0:
        return 0, 1
    # Recursively compute pair for floor(n/2)
    a, b = _fib_pair(n >> 1)
    # Apply doubling formulas
    c = a * ((b << 1) - a)          # F(2k)   = F(k) * (2*F(k+1) – F(k))
    d = a * a + b * b               # F(2k+1) = F(k)^2 + F(k+1)^2
    if n & 1:
        # n is odd: return (F(2k+1), F(2k+2))
        return d, c + d
    else:
        # n is even: return (F(2k), F(2k+1))
        return c, d


def fib(n: int) -> int:
    """Return the *n*‑th Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative index of the Fibonacci sequence.

    Returns
    -------
    int
        ``F(n)`` where ``F(0) == 0`` and ``F(1) == 1``.

    Raises
    ------
    ValueError
        If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    return _fib_pair(n)[0]


if __name__ == "__main__":
    # Simple demo: compute a few values and measure speed for a large n.
    import time
    test_vals = [0, 1, 2, 5, 10, 20, 50]
    for v in test_vals:
        print(f"fib({v}) = {fib(v)}")

    large_n = 200_000
    start = time.time()
    result = fib(large_n)
    elapsed = time.time() - start
    print(f"fib({large_n}) computed in {elapsed:.6f}s (digits: {len(str(result))})")
