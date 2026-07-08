"""Fibonacci numbers via fast doubling (O(log n)).

fib(0) = 0, fib(1) = 1.
Returns exact Python big integers. Stdlib only.
"""

from __future__ import annotations

import sys


def _fib_pair(n: int) -> tuple[int, int]:
    """Return (F(n), F(n+1)) using the fast-doubling identities.

    F(2k)   = F(k) * (2*F(k+1) - F(k))
    F(2k+1) = F(k+1)^2 + F(k)^2
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return (0, 1)

    # Iterative fast doubling: process bits of n from most to least
    # significant. Invariant: (a, b) = (F(m), F(m+1)) for the prefix m
    # built so far.
    a, b = 0, 1  # F(0), F(1)
    # Find the highest set bit.
    highest = n.bit_length() - 1
    for i in range(highest, -1, -1):
        # Double: (a, b) -> (F(2m), F(2m+1))
        # c = F(2m)   = a * (2*b - a)
        # d = F(2m+1) = a*a + b*b
        two_b_minus_a = (b << 1) - a
        c = a * two_b_minus_a
        d = a * a + b * b
        a, b = c, d
        if (n >> i) & 1:
            # Advance by one: (F(2m), F(2m+1)) -> (F(2m+1), F(2m+2))
            a, b = b, c + d
    return (a, b)


def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1).

    Uses fast doubling, O(log n) bigint operations. Exact.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    return _fib_pair(n)[0]


if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        n = int(args[0])
    else:
        n = 10
    print(fib(n))
