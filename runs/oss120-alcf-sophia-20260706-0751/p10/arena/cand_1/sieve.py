# sieve.py
"""Prime number generation using an efficient Sieve of Eratosthenes.

Provides a single public function:
    primes_up_to(n) -> List[int]
which returns a sorted list of all prime numbers ≤ n.

The implementation:
- Handles n < 2 by returning an empty list.
- Uses a ``bytearray`` to store primality of odd numbers only, cutting memory in half.
- Skips even numbers entirely (except the prime 2).
- Marks composites with slice assignment, which is fast in CPython.
- Relies only on the Python standard library.
"""

from __future__ import annotations
from math import isqrt
from typing import List


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of all prime numbers ≤ ``n``.

    Parameters
    ----------
    n: int
        Upper bound (inclusive). If ``n < 2`` the function returns an empty list.

    Returns
    -------
    List[int]
        Sorted list of primes less than or equal to ``n``.
    """
    if n < 2:
        return []

    # ``size`` represents the number of odd candidates up to ``n``.
    # Index ``i`` corresponds to the odd number ``2*i + 1``.
    size = (n + 1) // 2
    sieve = bytearray(b"\x01") * size
    # 1 is not prime.
    sieve[0] = 0

    limit = isqrt(n)
    # Only need to consider odd p up to sqrt(n).
    # The index of an odd p is (p // 2).
    for i in range(1, (limit // 2) + 1):
        if sieve[i]:
            p = 2 * i + 1
            # Start striking from p*p, which is always odd.
            start = (p * p) // 2
            # Number of positions to clear using slice assignment.
            step = p
            sieve[start::step] = b"\x00" * ((size - start - 1) // step + 1)

    # Collect primes: include 2 separately, then all odd indices still marked.
    primes: List[int] = [2]
    primes.extend(2 * i + 1 for i, is_prime in enumerate(sieve) if is_prime)
    return primes


if __name__ == "__main__":
    # Simple sanity check when run as a script.
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(primes_up_to(limit))
