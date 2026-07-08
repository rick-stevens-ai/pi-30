"""Efficient prime sieve.

Provides a single public function :func:`primes_up_to` which returns a sorted list of all
prime numbers less than or equal to ``n``.

The implementation is deliberately lightweight and uses only the Python standard
library.  For ``n`` up to a few million the algorithm runs in well under a second.

Key implementation details:

* ``bytearray`` is used as a mutable bitmap where ``0`` denotes a prime candidate
  and ``1`` marks a composite number.  ``bytearray`` is memory‑efficient (one
  byte per number) and fast for slice assignment.
* Even numbers greater than ``2`` are omitted from the sieving process.  The
  bitmap therefore only stores odd numbers, cutting the memory usage roughly in
  half.
* The classic *Sieve of Eratosthenes* is applied: for each prime ``p`` up to the
  square‑root of ``n`` we mark the multiples of ``p`` starting from ``p*p``.
* Edge cases (``n < 2``) return an empty list, and ``n == 2`` returns ``[2]``
  immediately without any further work.
"""

from __future__ import annotations
from math import isqrt
from typing import List

__all__ = ["primes_up_to"]


def _odd_sieve(limit: int) -> bytearray:
    """Return a bitmap for odd numbers up to *limit*.

    The bitmap has ``(limit // 2) + 1`` entries where index ``i`` corresponds to
    the odd number ``2*i + 1``.  A value of ``0`` means *potentially prime* and a
    value of ``1`` means *composite*.
    """
    size = (limit // 2) + 1  # include the entry for the highest odd <= limit
    sieve = bytearray(size)  # all zeroes → all odd numbers are initially assumed prime
    sieve[0] = 1  # mark number 1 as composite
    return sieve


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of all prime numbers ``<= n``.

    The function is optimised for the typical use‑case of sieving up to a few
    million.  It runs in ``O(n log log n)`` time and uses roughly ``n/2`` bytes of
    memory.

    Parameters
    ----------
    n: int
        Upper bound (inclusive) for the primes to generate.  ``n`` may be any
        non‑negative integer.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]

    # Initialise bitmap for odd numbers only.
    sieve = _odd_sieve(n)
    limit_sqrt = isqrt(n)

    # Only need to consider odd primes up to sqrt(n).
    # The index for an odd number ``p`` is ``p // 2``.
    for p in range(3, limit_sqrt + 1, 2):
        if sieve[p // 2] == 0:  # p is still marked as prime
            # Start marking from p*p, which is always odd.
            start = p * p
            step = p * 2  # skip even multiples
            # Convert the start number to an index in the bitmap.
            start_idx = start // 2
            sieve[start_idx::p] = b"\x01" * ((len(sieve) - start_idx - 1) // p + 1)
            # The slice assignment above marks every p-th odd number as composite.

    # Assemble the final list of primes.
    primes = [2]
    primes.extend([2 * i + 1 for i, flag in enumerate(sieve) if flag == 0 and 2 * i + 1 <= n])
    return primes
