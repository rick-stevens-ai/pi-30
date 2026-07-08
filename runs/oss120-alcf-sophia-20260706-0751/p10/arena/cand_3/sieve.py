'''sieve.py

Fast prime sieve implementation using a compact bytearray that stores only odd numbers.
The module exposes a single function ::

    primes_up_to(n) -> List[int]

which returns a sorted list of all prime numbers less than or equal to ``n``.

The implementation is fully based on the Python standard library and is tuned for
speed up to at least ``n = 2_000_000``.  It follows the classic "sieve of Eratosthenes"
optimised by:

* Storing only odd candidates in a ``bytearray`` (even numbers > 2 are known composites).
* Using slice assignment to clear multiples of each found prime in a single operation.
* Avoiding Python loops inside the inner clearing step.

Edge‑cases:

* ``n < 2`` returns an empty list.
* ``n == 2`` correctly returns ``[2]``.
* The function always returns a **new list** – callers may safely mutate the result.
'''

from __future__ import annotations
from typing import List
import math

__all__ = ["primes_up_to"]


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of all prime numbers ``<= n``.

    The algorithm works as follows:

    1. Handle the trivial cases ``n < 2`` and ``n == 2``.
    2. Create a ``bytearray`` ``is_prime`` where ``is_prime[i]`` represents the odd
       number ``2 * i + 1`` (so index ``0`` corresponds to ``1``).
    3. Run the sieve only up to ``sqrt(n)`` – the index of the square‑root is
       ``int(math.isqrt(n)) // 2`` because we store only odds.
    4. For each prime ``p = 2*i + 1`` found, clear its odd multiples using a
       slice assignment ``is_prime[start::p] = b"\x00" * count`` where ``start``
       is the index of ``p*p`` expressed in the odd‑only indexing scheme.
    5. Collect ``2`` (the only even prime) and then any odd number whose slot is
       still ``True``.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]

    # ``size`` is the number of odd integers from 1 up to n inclusive.
    # Number of odd integers from 1 up to n inclusive.
    # The count of odds <= n is (n + 1) // 2.
    size = (n + 1) // 2
    is_prime = bytearray(b"\x01") * size
    # 1 is not a prime.
    is_prime[0] = 0

    limit = int(math.isqrt(n))
    # Only need to consider odd factors up to sqrt(n).
    # Corresponding index in ``is_prime`` for a value ``p`` is ``p // 2``.
    max_i = limit // 2
    for i in range(1, max_i + 1):
        if is_prime[i]:
            p = 2 * i + 1
            # index of p*p in the odd‑only array:
            start = (p * p) // 2
            # Slice step size is the prime itself ``p`` because we step over odd multiples.
            is_prime[start::p] = b"\x00" * ((size - start - 1) // p + 1)

    # Gather results. 2 is always prime when n >= 2.
    primes = [2]
    primes.extend([2 * i + 1 for i in range(1, size) if is_prime[i]])
    return primes

# Simple self‑test executed when the module is run directly.
if __name__ == "__main__":
    import sys
    try:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    except ValueError:
        print("Usage: python sieve.py [n]")
        sys.exit(1)
    print(primes_up_to(limit))
