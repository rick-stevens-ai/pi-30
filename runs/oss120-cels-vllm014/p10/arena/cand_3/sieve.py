"""Efficient prime sieve implementation.

Provides a single public function ``primes_up_to`` which returns a sorted list of
prime numbers less than or equal to ``n``.

The implementation uses a classic incremental Sieve of Eratosthenes optimized
for speed and low memory consumption:

* ``bytearray`` stores a boolean flag for each odd candidate only – even numbers
  (except ``2``) are ignored entirely.
* Slicing with assignment is employed to mark composite numbers in bulk.
* ``n < 2`` correctly yields an empty list.

The algorithm runs comfortably within a few hundred milliseconds for ``n`` up to
2 000 000 on modern hardware and relies solely on the Python standard library.
"""

from __future__ import annotations

from math import isqrt
from typing import List

__all__ = ["primes_up_to"]


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of all prime numbers ``<= n``.

    Parameters
    ----------
    n: int
        Upper bound (inclusive) for the prime numbers to generate.

    Returns
    -------
    List[int]
        Sorted list of prime numbers not exceeding ``n``.  For ``n < 2`` the list
        is empty.
    """
    if n < 2:
        return []

    # ``2`` is the only even prime – handle it separately.
    if n == 2:
        return [2]

    # Only odd numbers are stored.  Index ``i`` corresponds to the integer
    # ``2*i + 1``.  We need slots for all odds up to ``n`` inclusive.
    size = (n // 2) + 1  # ``+1`` ensures the odd ``n`` itself is represented.
    sieve = bytearray(b"\x01") * size
    sieve[0] = 0  # ``1`` is not prime.

    limit = isqrt(n)
    # Iterate over odd candidates only.
    for i in range(3, limit + 1, 2):
        if sieve[i // 2]:
            # Start marking from i*i (the first composite not already marked).
            start = i * i
            step = i * 2  # Skip even multiples.
            # Compute slice start index in the odd-only array.
            start_idx = start // 2
            # Number of elements to clear in the slice.
            slice_len = (size - start_idx - 1) // (i) + 1
            sieve[start_idx::i] = b"\x00" * slice_len

    # Reconstruct prime list: include 2 and all odd numbers still marked.
    primes = [2]
    # Enumerate only the odd slots; convert back to the original integer.
    primes.extend(2 * i + 1 for i, is_prime in enumerate(sieve) if is_prime)
    # The comprehension may include a number > n when ``n`` is even; trim it.
    if primes[-1] > n:
        primes.pop()
    return primes
