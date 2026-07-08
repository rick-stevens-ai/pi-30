# sieve.py
"""Efficient prime sieve implementation.

Provides a single public function:
    primes_up_to(n) -> List[int]
which returns the sorted list of all prime numbers less than or equal to ``n``.

The implementation is tuned for speed on inputs up to a few million:
* Uses a ``bytearray`` as a compact mutable bit‑set.
* Stores only odd numbers (even numbers >2 are known composites), halving
  memory usage and reducing the number of iterations.
* Marks composites using slice assignment, which is implemented in C and
  therefore much faster than a Python loop.
* Handles edge cases (``n < 2``) gracefully by returning an empty list.

The algorithm runs in ``O(n log log n)`` time and ``O(n)`` memory, which
is optimal for the classic Sieve of Eratosthenes.
"""

from __future__ import annotations

from typing import List

__all__ = ["primes_up_to"]


def primes_up_to(n: int) -> List[int]:
    """Return a list of all prime numbers ``<= n``.

    Parameters
    ----------
    n: int
        Upper bound (inclusive) for the primes to generate. ``n`` may be any
        non‑negative integer. For ``n < 2`` the function returns ``[]``.

    Returns
    -------
    List[int]
        Sorted list of prime numbers not greater than ``n``.

    Notes
    -----
    * The implementation stores only odd candidates in the sieve array.
      Index ``i`` of the ``bytearray`` corresponds to the number ``2*i + 3``.
    * ``bytearray`` values are ``0`` for potential primes and ``1`` for known
      composites. ``0`` is the default state, so we only need to write ``1``
      for composites.
    * Composite marking uses slice assignment:
          sieve[start::step] = b"\x01" * count
      which is executed in C and is therefore far faster than a Python loop.
    * After sieving, the resulting list is built by concatenating ``2`` (if
      within range) with the odd numbers that remain unmarked.
    """

    if n < 2:
        return []

    # 2 is the only even prime.
    primes: List[int] = [2] if n >= 2 else []

    # For n == 2 we can return early – no odd numbers to process.
    if n == 2:
        return primes

    # Number of odd candidates from 3 up to n inclusive.
    # Example: n=9 -> odds = 3,5,7,9 => count = (9-3)//2 + 1 = 4
    odd_count = (n - 3) // 2 + 1
    sieve = bytearray(odd_count)  # 0 = potential prime, 1 = composite

    # Upper bound for the base primes we need to iterate over.
    # Only need to consider primes up to sqrt(n).
    import math
    limit = int(math.isqrt(n))
    # Convert limit to the corresponding index in the odd-only array.
    # If limit < 3 we skip the loop entirely.
    if limit >= 3:
        # The index of the number p in sieve is (p - 3) // 2.
        max_index = (limit - 3) // 2
        for i in range(max_index + 1):
            if sieve[i]:
                continue  # already marked as composite
            p = 2 * i + 3  # actual prime value
            # Start marking from p*p. Convert that to an index in the odd-only array.
            start = (p * p - 3) // 2
            step = p  # step in terms of odd indices corresponds to p (since we skip evens)
            # Calculate how many entries we will mark to allocate the filler bytes.
            # The slice goes from start to the end of the array with step size `step`.
            sieve[start::step] = b"\x01" * ((odd_count - start - 1) // step + 1)

    # Collect remaining primes from the sieve.
    # Each index i that remains 0 corresponds to prime 2*i + 3.
    primes.extend([2 * i + 3 for i, is_comp in enumerate(sieve) if not is_comp])
    return primes

# Simple self‑test when run as a script.
if __name__ == "__main__":
    import sys
    try:
        limit = int(sys.argv[1])
    except Exception:
        print("Usage: python sieve.py <n>")
        sys.exit(1)
    print(primes_up_to(limit))
