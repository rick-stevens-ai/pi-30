"""
Sieve of Eratosthenes implementation.

Exposes:
    primes_up_to(n: int) -> List[int]
        Return a list of all prime numbers ≤ n, sorted ascending.

The algorithm is optimised for the common case with an upper limit of
2 000 000.  It uses a :class:`bytearray` as a bitset and explicitly skips
even numbers to halve memory usage and reduce loop iterations.

Key optimisations:

* Mark all even numbers greater than 2 as composite from the start using
  slice assignment on the bytearray.
* Iterate only over odd candidate primes up to √n, again using slice
  assignment for marking multiples.
* For very small inputs (``n < 2``) return an empty list immediately.
"""

from __future__ import annotations

from math import isqrt
from typing import List


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of prime numbers ≤ *n*.

    Parameters
    ----------
    n:
        The upper bound (inclusive).  ``negative`` values are treated as
        zero; ``0`` and ``1`` return an empty list.

    Returns
    -------
    List[int]
        All primes ≤ *n* in ascending order.

    The implementation follows the classic Sieve of Eratosthenes but
    removes all even numbers except 2 from consideration.  A
    :class:`bytearray` is used to store primality flags; ``1`` denotes a
    prime candidate, ``0`` denotes composite.
    """

    if n < 2:
        return []

    # Special‑casing the only even prime keeps code simpler and keeps
    # the array size small for odd numbers.
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0] = sieve[1] = 0          # 0 and 1 are not primes

    if n >= 4:
        # Mark all even numbers > 2 as composite.
        sieve[4 : n + 1 : 2] = b"\x00" * ((n - 4) // 2 + 1)

    limit = isqrt(n)
    # Only iterate over odd candidates.  ``range(3, limit+1, 2)``
    # covers all potential prime bases for sieving.
    for p in range(3, limit + 1, 2):
        if sieve[p]:
            start = p * p
            step = p << 1   # 2*p – skip even multiples
            sieve[start : n + 1 : step] = b"\x00" * ((n - start) // step + 1)

    # Convert to list; ``enumerate`` over bytearray gives int values.
    return [num for num, is_prime in enumerate(sieve) if is_prime]

# The module is intentionally free of side effects so it can safely be
# imported into other projects.  If executed as a script, demonstrate
# the function with a tiny example.
if __name__ == "__main__":
    import sys

    try:
        bound = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    except ValueError:
        print("Please provide an integer upper limit.\nUsage: python sieve.py <N>")
        sys.exit(1)

    primes = primes_up_to(bound)
    print(f"Primes <= {bound}: {primes}")
