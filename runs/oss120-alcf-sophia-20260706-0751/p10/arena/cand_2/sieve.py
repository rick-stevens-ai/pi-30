"""sieve.py

Efficient prime generation up to a given limit.

Provides a single public function

    primes_up_to(n) -> List[int]

which returns a sorted list of all prime numbers ``p`` such that ``p <= n``.

The implementation is a classic *odd‑only* Sieve of Eratosthenes using a
``bytearray`` for memory efficiency and slice assignment for speed.  It is
optimised for the typical interview/algorithmic workload of generating all
primes up to a few million – for example ``n = 2_000_000`` runs well under a
second on modern hardware.

Only the Python standard library is used.
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
        Upper bound (inclusive).  ``n`` may be any non‑negative integer.

    Returns
    -------
    List[int]
        Sorted list of primes ``p`` where ``p <= n``.  For ``n < 2`` the list
        is empty.

    Notes
    -----
    * The algorithm stores only **odd** numbers in the sieve to halve the
      memory footprint.
    * ``bytearray`` entries are ``0`` for *potential prime* and ``1`` for
      *composite*.
    * Slice assignment (``sieve[start::step] = b"\x01" * count``) marks the
      multiples of a discovered prime in bulk, which is considerably faster
      than a Python ``for`` loop.
    """
    if n < 2:
        return []

    # ``limit`` is the number of odd candidates up to ``n`` inclusive.
    # Mapping: index i -> number 2*i + 1.
    limit = (n + 1) // 2
    sieve = bytearray(limit)  # 0 = prime candidate, 1 = composite
    sieve[0] = 1  # 1 is not a prime

    # Upper bound for checking – only odd primes up to sqrt(n) are needed.
    max_p = isqrt(n)
    # ``max_i`` is the index of ``max_p`` in the odd‑only representation.
    max_i = max_p // 2

    for i in range(1, max_i + 1):
        if sieve[i] == 0:  # i corresponds to a prime p = 2*i + 1
            p = 2 * i + 1
            # Index of p*p in the odd‑only array.
            start = (p * p) // 2
            step = p
            # Number of elements to set – compute length of the slice.
            count = (limit - start - 1) // step + 1
            sieve[start::step] = b"\x01" * count

    # Gather primes: 2 is the only even prime.
    primes = [2]
    primes.extend(2 * i + 1 for i in range(1, limit) if sieve[i] == 0)
    return primes


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sieve.py <n>")
        sys.exit(1)
    try:
        bound = int(sys.argv[1])
    except ValueError:
        print("<n> must be an integer")
        sys.exit(1)
    print(primes_up_to(bound))
