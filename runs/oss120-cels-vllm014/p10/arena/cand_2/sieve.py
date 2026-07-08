"""sieve.py
================
Provides a fast implementation of the Sieve of Eratosthenes that returns all
prime numbers less than or equal to a given integer ``n``.

The public API consists of a single function:

    primes_up_to(n) -> List[int]

* ``n`` may be any non‑negative integer.
* For ``n < 2`` the function returns an empty list.
* The returned list is sorted in increasing order.
* The implementation is optimised for speed up to at least ``n = 2_000_000``
  using a ``bytearray`` bitmap, skipping even numbers, and slice‑assignment to
  clear multiples.  Only the standard library is used.
"""

from __future__ import annotations

from math import isqrt
from typing import List

__all__ = ["primes_up_to"]


def _odd_sieve(limit: int) -> bytearray:
    """Return a bitmap for odd numbers up to ``limit``.

    The bitmap represents only odd numbers starting from 3.  ``bitmap[i]`` is
    ``1`` if the number ``2*i + 3`` is still considered prime, ``0`` otherwise.
    The length of the bitmap is ``(limit - 1) // 2`` – exactly the count of odd
    numbers in ``[3, limit]``.
    """
    # Number of odd candidates >=3 and <= limit
    size = (limit - 1) // 2
    # Start with all bits set (potential primes)
    bitmap = bytearray(b"\x01") * size
    # Upper bound for the base prime we need to process
    bound = isqrt(limit)
    # Iterate over odd indices; the actual number is 2*i + 3
    for i in range((bound - 3) // 2 + 1):
        if bitmap[i]:
            p = 2 * i + 3
            # The first multiple of p that is >= p*p and odd is p*p.
            start = (p * p - 3) // 2
            # Step size in the bitmap corresponds to p (since we only store odds)
            bitmap[start::p] = b"\x00" * ((size - start - 1) // p + 1)
    return bitmap


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of all prime numbers ``<= n``.

    The algorithm is a classic Sieve of Eratosthenes with a few optimisations:

    * Even numbers > 2 are ignored – they are never prime.
    * A ``bytearray`` is used as a mutable bitmap; this is memory‑efficient and
      allows fast slice assignment to clear multiples.
    * Only prime candidates up to ``sqrt(n)`` are used as sieving bases.
    * The final list is constructed by expanding the bitmap back to actual
      integer values.

    Parameters
    ----------
    n: int
        Upper bound (inclusive) for the primes to generate.  ``n`` must be a
        non‑negative integer; a ``ValueError`` is raised otherwise.

    Returns
    -------
    List[int]
        Sorted list of prime numbers less than or equal to ``n``.  For ``n < 2``
        the list is empty.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    if n < 2:
        return []

    # 2 is the only even prime – handle it up‑front
    primes: List[int] = [2]

    if n == 2:
        return primes

    # Build bitmap for odd numbers only
    bitmap = _odd_sieve(n)
    # Convert bitmap back to actual prime numbers (odd values only)
    primes.extend([2 * i + 3 for i, is_prime in enumerate(bitmap) if is_prime])
    return primes

# Simple self‑test when run as a script
if __name__ == "__main__":
    import sys
    try:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    except ValueError:
        print("Usage: python sieve.py [limit]")
        sys.exit(1)
    print(primes_up_to(limit))
