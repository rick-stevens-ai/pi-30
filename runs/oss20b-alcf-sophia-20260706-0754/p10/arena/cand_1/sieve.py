"""
Sieve of Eratosthenes implementation.

This module exposes :func:`primes_up_to` which returns a sorted list
of all prime numbers less than or equal to *n*.

The implementation is purposefully small and efficient for n up to a
few million:

* Uses a :class:`bytearray` to store only odd numbers – saving both
  memory and operations.
* Marks composites with slice assignment which is faster than
  iterating and setting each element individually.
* Handles edge cases: ``n < 2`` returns an empty list and ``n == 2``
  returns `[2]`.

Only the Python standard library is required.
"""

from __future__ import annotations

import math


__all__ = ["primes_up_to"]


def primes_up_to(n: int) -> list[int]:
    """Return a sorted list of all prime numbers ≤ *n*.

    Parameters
    ----------
    n:
        Upper bound for the primes.

    Returns
    -------
    list[int]
        Sorted list of primes not exceeding :data:`n`.

    Notes
    -----
    * For ``n < 2`` the result is an empty list.
    * For ``n == 2`` the result is ``[2]``.
    * The algorithm is a classic sieve of Eratosthenes implemented in a
      compact and fast way.  Composites are marked using slice
      assignment on a :class:`bytearray` that stores only odd numbers.
    """

    if n < 2:
        return []
    if n == 2:
        return [2]

    # Represent only odd numbers starting from 3.
    # index i corresponds to number 2*i + 3.
    sieve_len = (n - 1) // 2  # number of odd integers in [3, n]
    sieve = bytearray([1]) * sieve_len

    limit = int(math.isqrt(n))
    # iterate over odd p values
    for p in range(3, limit + 1, 2):
        idx = (p - 3) // 2
        if sieve[idx]:
            # start marking from p*p
            start = (p * p - 3) // 2
            step = p
            sieve[start::step] = bytearray(len(sieve[start::step]))

    primes = [2] + [2 * i + 3 for i, prime in enumerate(sieve) if prime]
    return primes


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Generate primes up to an integer.")
    parser.add_argument("n", type=int, help="Upper bound (inclusive).")
    args = parser.parse_args()

    primes = primes_up_to(args.n)
    print(f"{len(primes)} primes up to {args.n}")
    print(primes)
    sys.exit(0)
