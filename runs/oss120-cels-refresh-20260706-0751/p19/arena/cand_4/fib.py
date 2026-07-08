# fib.py
"""Compute Fibonacci numbers using the fast‑doubling algorithm.

The function :func:`fib` returns the *n*‑th Fibonacci number with
`fib(0) == 0` and `fib(1) == 1`.  It runs in :math:`O(\log n)` time and
uses only Python's built‑in arbitrary‑precision integers, so it can handle
very large *n* (e.g., ``n = 200_000``) instantly.

The implementation follows the classic fast‑doubling recurrence:

```
F(2k)   = F(k) * [2*F(k+1) – F(k)]
F(2k+1) = F(k)^2 + F(k+1)^2
```

Both values ``(F(k), F(k+1))`` are computed recursively, giving a
pair‑wise result that avoids the linear recursion depth of the naive
definition.
"""

from __future__ import annotations

__all__ = ["fib"]


def fib(n: int) -> int:
    """Return the *n*‑th Fibonacci number.

    Parameters
    ----------
    n: int
        Index of the Fibonacci number to compute.  Must be a non‑negative
        integer.

    Returns
    -------
    int
        The *n*‑th Fibonacci number.

    Raises
    ------
    ValueError
        If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")

    def _fib_pair(k: int) -> tuple[int, int]:
        """Return the pair ``(F(k), F(k+1))`` using fast doubling.

        This helper is tail‑recursive in the mathematical sense: each call
        reduces ``k`` roughly by half, guaranteeing :math:`O(\log k)` depth.
        """
        if k == 0:
            return (0, 1)
        # Recursively compute (F(m), F(m+1)) where m = k // 2
        a, b = _fib_pair(k >> 1)
        # Apply the doubling formulas
        c = a * ((b << 1) - a)        # F(2m)
        d = a * a + b * b            # F(2m + 1)
        if k & 1:
            # k is odd: return (F(2m+1), F(2m+2))
            return (d, c + d)
        else:
            # k is even: return (F(2m), F(2m+1))
            return (c, d)

    return _fib_pair(n)[0]

# Simple sanity check when the module is executed directly
if __name__ == "__main__":
    import sys
    try:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    except ValueError:
        print("Please provide a non‑negative integer.")
        sys.exit(1)
    print(fib(n))
