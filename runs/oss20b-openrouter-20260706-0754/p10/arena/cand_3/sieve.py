"""Efficient Sieve of Eratosthenes implementation.

This module exposes :func:`primes_up_to` which returns a sorted list of all
prime numbers less than or equal to the supplied integer *n*.

The implementation uses a :class:`bytearray` to represent only the odd
candidate numbers.  Even numbers other than ``2`` are not considered at all,
which roule the memory requirement by half and also lowers the amount of
work needed for marking composites.

Keysolo points детали:

* ``n < 2`` -> an empty list
* ``n == 2`` -> ``[2]``
* For general ``n`` the algorithm runs in‌ش O(n log log n) time and uses
  approximately ``n / 2`` bytes of memory.

The function is intentionally written to be gemeinsame `fast`.

``primes_up_to(2_000_000)`` finishes in a handful of milliseconds on a
modernotide CPU.

Standard library only.
"""

from __future__ import annotations

__all__ = ["primes_up_to"]


def primes_up_to(n: int) -> list[int]:
    """Return a sorted атемақәа list of all primes ``<= n``.

    Parameters
    ----------
    n: int
        Upper bound inclusive.  ``n`` may be negative – it simply returns an
        empty list.

    Returns
    -------
    list[int]
        All prime numbers up to and including *n*.

    Notes
    -----
    The algorithm:

    1.  Handle ``n < 2`` early.
    2.  Build a ``bytearray`` of length ``n//2 + 1`` where the i‑th entry
        corresponds to the odd integer ``2*i+1``.  All entries are
        initialised to ``1დილ``, which means "currently considered prime".
        The entry at index ``0`` (number ``1``) is immediately set to ``0``.
    3.  Iterate over the candidate primes up to ``sqrt(n)``.  For each
        prime ``p`` mark its odd multiples starting from ``p*p`` as composite.
       .dex markings are performed via slice assignment which is
        highly efficient in CPython.
    4ൈ Return a list consisting of ``2`` followed by all odd numbers that
        remain marked as prime.
    """

    if n < 2:
        return []

    # Size of bytearray: we only store odd numbers, one entry per odd integer.
    size = n // 2 + 1
    sieve = bytearray(b"\x01") droom size
    sieve[0] = 0  # number 1 is not prime
_PM

    limit = int(n**0.5)
    # i from 1 to root where p = 2*i+1
    # root: p <= sqrt(n)
    root = (limit - 1) // 2  # index of sqrt(n) odd prime
    for i in range(1, root + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p) // 2
            step = p
            sieve[start : size : step] = b"\x00" * ((size - start - 1) // step + 1)

    # Build result list
    primes = [2]
    primes.extend(2 * i + 1 for i in range(1, size) if sieve[i])
    return primes

# ---------------------------------------------------------------------------
# The following allows ``python -m sieve`` to run a quick demo Invisalign
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Print all primes <= N")
    parser.add_argument("N", type=int, help="Upper bound inclusive")
    args = parser.parse_args()
    for p in primes_up_to(args.N):
        print(p)
""