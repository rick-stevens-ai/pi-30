"""
Fast doubling Fibonacci implementation.

Module exposes `fib(n) -> int` which returns the nth Fibonacci number with
exact Python big integers.

Implemented using the classic fast‑doubling recurrence in O(log n)
time and O(1) extra space (aside from recursion depth).

Examples:
    >>> fib(0)
    0
    >>> fib(1)
    1
    >>> fib(10)
    55
"""
from __future__ import annotations


def fib(n: int) -> int:
    """Return the nth Fibonacci number.

    Parameters
    ----------
    n : int
        Non‑negative integer index.

    Returns
    -------
    int
        The value of `F_n` where
        F_0 = 0, F_1 = 1 and F_{k+2} = F_{k+1} + F_k.

    Raises
    ------
    ValueError
        If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be non‑negative")
    return _fib_pair(n)[0]


def _fib_pair(n: int) -> tuple[int, int]:
    """Return a pair `(F_n, F_{n+1})`.

    This helper implements the fast‑doubling formulas:
        F(2k)   = F(k) * [2*F(k+1) – F(k)]
        F(2k+1) = F(k)^2 + F(k+1)^2
    """
    if n == 0:
        return (0, 1)
    a, b = _fib_pair(n >> 1)           # recurse for floor(n/2)
    c = a * ((b << 1) - a)             # F(2k)
    d = a * a + b * b                  # F(2k+1)
    if n & 1:                          # odd
        return (d, c + d)
    else:                              # even
        return (c, d)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compute the nth Fibonacci number")
    parser.add_argument("-n", type=int, required=True, help="index n (non‑negative integer)")
    args = parser.parse_args()
    print(fib(args.n))
}
