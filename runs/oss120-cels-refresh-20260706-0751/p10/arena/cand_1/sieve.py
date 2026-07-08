"""sieve.py

Implementation of the Sieve of Eratosthenes returning all prime numbers
up to (and including) a given limit ``n``.

The implementation is optimised for speed while staying within the Python
standard library:

* ``bytearray`` is used to store a boolean mask for odd numbers only – this
  reduces memory usage by roughly a factor of two.
* The classic inner‑loop is replaced by a slice assignment which zeroes out
  multiples of a prime in a single operation.
* ``2`` is handled separately so that the inner loop can skip all even
  numbers.

The public API consists of a single function ``primes_up_to`` which returns a
sorted list of primes ``<= n``.  Edge cases (``n < 2``) are handled gracefully
by returning an empty list.
"""

from __future__ import annotations
from math import isqrt
from typing import List


def primes_up_to(n: int) -> List[int]:
    """Return a list of all prime numbers less than or equal to ``n``.

    The algorithm runs in ``O(n log log n)`` time and uses ``O(n)`` bits of
    memory (implemented with a ``bytearray``).  It is fast enough to generate
    all primes up to two million in well under a second on modest hardware.

    Parameters
    ----------
    n: int
        Upper inclusive bound for the primes to be returned.

    Returns
    -------
    List[int]
        Sorted list of prime numbers ``<= n``.  For ``n < 2`` the list is
        empty.
    """
    if n < 2:
        return []

    # ``2`` is the only even prime – store it separately and work only with odd
    # numbers from here on.
    primes: List[int] = [2]

    # Number of odd candidates we need to represent: 1, 3, 5, ..., n (if n is odd)
    size = (n + 1) // 2  # index i represents the odd number 2*i + 1
    sieve = bytearray(b"\x01") * size
    sieve[0] = 0  # 1 is not prime

    limit = isqrt(n)
    # Only iterate over odd bases up to sqrt(n).  ``i`` corresponds to the odd
    # number ``p = 2*i + 1``.
    for i in range(1, (limit // 2) + 1):
        if sieve[i]:
            p = 2 * i + 1
            # Start crossing off at p*p.  Convert that number back to an index
            # in the ``sieve`` (which stores only odd numbers).
            start = (p * p) // 2
            # Slice assignment zeros out every ``p``‑th entry from ``start``.
            sieve[start::p] = b"\x00" * ((size - start - 1) // p + 1)

    # Append the remaining odd primes to the result list.
    primes.extend(2 * i + 1 for i, is_prime in enumerate(sieve) if is_prime)
    return primes


if __name__ == "__main__":
    # Simple sanity check when the module is executed directly.
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    print(primes_up_to(limit))
