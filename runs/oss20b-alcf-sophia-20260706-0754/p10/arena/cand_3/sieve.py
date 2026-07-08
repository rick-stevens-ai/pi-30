"""Efficient prime sieve implementation.

This module exposes :func:`primes_up_to` which returns a sorted
list of all primes less than or equal to ``n``.

The implementation is a classic Eratosthenes sieve with a few
micro‑optimisations:

* ``bytearray`` is used for memory efficiency.
* Even numbers greater than 2 are marked in one slice assignment.
* Subsequent sieving also uses slice assigns to jump over
  composites of an odd prime.
* The algorithm runs in :math:`O(n \log \log n)` time and uses
  roughly 1 byte per number, making it comfortably fast for
  limits up to several millions.

Only the Python standard library is imported.
"""

from __future__ import annotations

import math

__all__ = ["primes_up_to"]


def primes_up_to(n: int) -> list[int]:
    """Return a list of all primes ``p`` such that ``p <= n``.

    Parameters
    ----------
    n : int
        Upper bound for the sieve.  ``n`` must be non‑negative.  If
        ``n < 2`` the function returns an empty list.

    Returns
    -------
    list[int]
        Sorted list of primes up to ``n``.
    """
    if n < 2:
        return []

    # ``sieve[i]`` is ``1`` if ``i`` is currently considered a
    # potential prime, ``0`` otherwise.
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0] = sieve[1] = 0

    # Mark all even numbers > 2 as composite in one go.
    # The number of such even numbers is ``n // 2 - 1``.
    if n >= 4:
        sieve[4 : n + 1 : 2] = b"\x00" * (n // 2 - 1)

    limit = int(math.isqrt(n))
    for p in range(3, limit + 1, 2):
        if sieve[p]:
            # Mark the multiples of p, starting from p*p.
            start = p * p
            step = 2 * p
            count = ((n - start) // step) + 1
            sieve[start : n + 1 : step] = b"\x00" * count

    # Collect primes: start with 2, then all odd indices marked as prime.
    primes: list[int] = [2]
    primes.extend(i for i in range(3, n + 1, 2) if sieve[i])
    return primes

# Simple sanity check when executed as a script.
if __name__ == "__main__":
    import sys
    try:
        limit = int(sys.argv[1])
    except Exception:
        limit = 100
    print(f"Primes up to {limit}:", primes_up_to(limit))
