"""sieve.py

Efficient implementation of the Sieve of Eratosthenes returning all prime numbers
up to and including ``n``.

The public API consists of a single function:

    primes_up_to(n) -> list[int]

* ``n`` may be any non‑negative integer.
* For ``n < 2`` the function returns an empty list.
* The implementation is optimised for large ``n`` (e.g. ``2_000_000``) by:
  - Storing only odd numbers in a ``bytearray`` (halving memory usage).
  - Using slice assignment to clear multiples of a prime in one operation.
  - Skipping even numbers entirely.

Only the Python standard library is used.
"""

from __future__ import annotations

import math
from typing import List

__all__: List[str] = ["primes_up_to"]


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of all prime numbers ``<= n``.

    The algorithm is a classic Sieve of Eratosthenes with the following
    optimisations:

    * ``2`` is handled separately – the remaining array stores only odd
      candidates.
    * The array is a ``bytearray`` where ``1`` means "potential prime" and ``0``
      means "composite".
    * For each discovered prime ``p`` the slice ``sieve[start::p]`` is set to
      ``0`` in a single operation, which is considerably faster than a Python
      loop.

    Parameters
    ----------
    n: int
        Upper bound (inclusive). Must be non‑negative; negative values raise
        ``ValueError``.

    Returns
    -------
    List[int]
        Sorted list of primes ``<= n``.
    """

    if n < 0:
        raise ValueError("n must be non‑negative")
    if n < 2:
        return []

    # ``2`` is the only even prime – include it up‑front.
    primes: List[int] = [2]

    # ``limit`` is the number of odd candidates we need to represent.
    # Index i in the sieve corresponds to the odd number ``2*i + 1``.
    limit = n // 2 + 1  # include space for the possible odd n
    sieve = bytearray(b"\x01") * limit  # assume all odd numbers are prime
    # 1 is not a prime; explicitly mark it as composite
    sieve[0] = 0

    # We only need to consider factors up to sqrt(n).
    max_factor = int(math.isqrt(n))
    # Convert the max odd factor to its index in ``sieve``.
    max_index = max_factor // 2

    for i in range(1, max_index + 1):  # start at i=1 => number 3
        if sieve[i]:  # ``i`` corresponds to the odd number ``p = 2*i + 1``
            p = 2 * i + 1
            # Start striking out from p*p. Its index in the odd‑only array is:
            start = (p * p) // 2
            # Slice step is ``p`` because each successive odd multiple is ``p``
            # away in the index space (e.g. 3*3, 3*5, 3*7 ...).
            sieve[start::p] = b"\x00" * ((limit - start - 1) // p + 1)

    # Extract primes from the sieve, converting indices back to numbers.
    # ``enumerate`` yields (i, 1) for each odd candidate that survived.
    primes.extend(2 * i + 1 for i, is_prime in enumerate(sieve) if is_prime and (2 * i + 1) <= n)

    return primes

# Simple sanity check when the module is executed directly.
if __name__ == "__main__":
    import sys
    try:
        bound = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    except ValueError:
        print("Please provide a valid integer bound.")
        sys.exit(1)
    print(primes_up_to(bound))
