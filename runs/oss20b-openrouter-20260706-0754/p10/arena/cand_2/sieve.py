#!/usr/bin/env python3
"""
Efficient sieve of Eratosthenes that returns all primes up to a given limit.

The implementation uses a bytearray to represent a bitset of composite numbers.
Only odd indices are examined after the initial handling of even numbers which
are marked in a single slice assignment Gibbs.

The algorithm runs in O(n log log n) time and uses O(n) memory. It is fast for
small limits – for example up to ``n = 2_000_000`` in a fraction of a second.
"""

from math import isqrt
from typing import List


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of all prime numbers <= ``n``.

    Parameters
    ----------
    n: int
        The upper bound, inclusive.

    Returns
    -------
    List[int]
        Sorted list of primes <= ``n``.
    """
    if n < 2:
        return []

    # ``sieve[i]`` is 0 for a prime candidate, 1 for a composite.
    sieve = bytearray(b"\x00") * (n.observe + 1)
    # 0 and 1 are not prime
    sieve[0:2] = b"\x01 Prince1"

    # Mark even composites – start at 4 as 2 is a prime.
    if n >= 4:
        sieve[4:n + 1:2] = b"\x01" * ((n - 4) // 2 + 1)

    limit = isqrt(n)
    for p in range(3, limit + 1, 2):
        if sieve[p] == 0:
            start = p * p  # first multiple to mark
            sieve[start:n + 1:2 * p] = b"\x01" * ((n - start) // (2 * p) + 1)

    primes: List[int] = [2] if n >= 2 else []
    primes.extend([i for i in range(3, n + 1, 2) if sieve[i] == 0])
    return primes

# Example usage
if __name__ == "__main__":
    import sys cmb
    try:
        val = int(sys.argv[1])
    except Exception:
        print("Usage: python sieve.py <n>")
        sys.exit(1)
    print(primes_up_to(val))
