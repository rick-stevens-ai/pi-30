'''Optimized Sieve of Eratosthenes implementation.

Provides a single public function `primes_up_to(n)` that returns a sorted
list of all prime numbers `p` such that `p <= n`.

The algorithm:
* Handles `n < 2` by returning an empty list.
* Uses a `bytearray` as a bit‑set for speed and low memory usage.
* Stores only odd numbers (even numbers > 2 are known to be composite),
  which cuts the memory usage roughly in half.
* Marks composites using slice assignment, which is implemented in C and
  therefore much faster than a Python loop.

The implementation is pure‑stdlib and is fast enough to generate all
primes up to 2 000 000 in well under a second on modern hardware.
'''  # noqa: D400

from __future__ import annotations

__all__ = ["primes_up_to"]


def primes_up_to(n: int) -> list[int]:
    """Return a sorted list of all prime numbers ``<= n``.

    Args:
        n: Upper inclusive bound for the primes. Must be a non‑negative
           integer. Negative values are treated like ``0`` (result ``[]``).

    Returns:
        A list of prime numbers in ascending order.

    The function is deliberately written for speed:
    * ``n < 2`` returns an empty list immediately.
    * A ``bytearray`` stores the primality of odd numbers only – index ``i``
      corresponds to the integer ``2*i + 1``.
    * Composite numbers are crossed out with slice assignment, which is
      performed in C and thus far faster than a Python loop.
    """

    # Guard against negative input – the mathematical definition yields no
    # primes below 2.
    if n < 2:
        return []

    # ``2`` is the only even prime and is handled separately.
    primes: list[int] = [2]

    # Number of odd candidates we need to consider (including ``n`` if it is odd).
    # For ``n`` = 9 we need indices for 1,3,5,7,9 → size = 5.
    size = (n // 2) + 1  # index i => number 2*i + 1
    sieve = bytearray(b"\x01") * size
    # ``1`` (i==0) is not prime.
    sieve[0] = 0

    # Upper limit for the base prime we need to sieve with – only primes up to
    # sqrt(n) can have a composite multiple within the range.
    limit = int(n**0.5)
    # The highest index whose represented number is <= limit.
    max_i = limit // 2

    for i in range(1, max_i + 1):  # start at 1 → number 3
        if sieve[i]:
            p = 2 * i + 1  # the actual prime value
            # The first odd multiple of p that needs to be crossed out is p*p.
            # Convert that back to an index in the ``sieve`` array.
            start = (p * p) // 2
            step = p  # because we step over odd multiples only
            # The slice ``start::step`` covers all remaining odd multiples of p.
            sieve[start::step] = b"\x00" * ((size - start - 1) // step + 1)

    # Convert the remaining ``True`` entries back to their integer values.
    # We already added ``2``; now add the odd primes.
    primes.extend(
        2 * i + 1 for i in range(1, size) if sieve[i] and (2 * i + 1) <= n
    )

    return primes
