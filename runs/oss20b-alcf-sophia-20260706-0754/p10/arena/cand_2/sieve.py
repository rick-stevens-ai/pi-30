"""Efficient sieve implementation.

This module exposes :func:`primes_up_to(n)` which returns a sorted list of all
prime numbers less than or equal to ``n``.

The implementation follows the classic bit‑set sieve but uses a
:class:`bytearray` for memory efficiency and to take advantage of fast slice
assignment.  Only odd numbers are represented – 2 is handled separately.

``primes_up_to`` accepts ``n`` as ``int`` and returns ``list[int]``.  It
handles edge cases (``n < 2``) by returning an empty list.

Examples
--------

>>> primes_up_to(10)
[2, 3, 5, 7]
>>> primes_up_to(1)
[]

Performance note
-----------------

Up to ``n = 2,000,000`` the sieve runs comfortably under a second on a
modern CPU using only the standard library.
"""

from __future__ import annotations

__all__ = ["primes_up_to"]


def primes_up_to(n: int) -> list[int]:
    """Return a sorted list of all primes ``<= n``.

    Parameters
    ----------
    n:
        Upper bound; inclusive.

    Returns
    -------
    list[int]
        Sorted list of primes up to ``n``.

    Notes
    -----
    *  Even numbers are skipped to half the memory usage and to speed up the
       process.  2 is added manually.
    *  The sieve is stored in a :class:`bytearray` where index ``i``
       represents the odd number ``2*i + 1``.  ``sieve[0]`` corresponds to
       ``1`` and is always set to ``False``.
    *  Slice assignment is used to strike out multiples of each found
       prime.
    """
    if n < 2:
        return []

    # Number of odd numbers up to ``n`` (including 1). ``size`` is the length
    # of the bytearray.
    size = (n + 1) // 2
    sieve = bytearray([True]) * size
    sieve[0] = False  # 1 is not prime

    limit = int(n**0.5)
    for p in range(3, limit + 1, 2):
        if sieve[p // 2]:  # p is prime
            step = p
            # Index in the sieve corresponding to p*p
            start = (p * p) // 2
            # Mark all odd multiples of p as composite.
            sieve[start :: step] = bytearray(len(sieve[start :: step]))

    primes = [2]
    # Collect odd primes from sieve.
    primes.extend(2 * i + 1 for i in range(1, size) if sieve[i])
    return primes

# If this module is executed directly, run a small sanity check.
if __name__ == "__main__":
    import sys
    try:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    except ValueError:
        limit = 100
    print(
        f"Primes up to {limit}:\n",
        primes_up_to(limit),
    )
