"""Sieve of Eratosthenes implementation with fast bytearray slicing.

Exports:
    primes_up_to(n) -> list[int]: all primes <= n, sorted ascending.
"""

from math import isqrt
from typing import List


def primes_up_to(n: int) -> List[int]:
    """
    Return a sorted list of all prime numbers <= n using an optimized
    bytearray sieve.

    The implementation:
      * Handles n < 2 by returning [] immediately.
      * Uses a bytearray for memory efficiency and slice assignment to mark
        multiples, which is fast in CPython.
      * Skips even numbers entirely after handling the special case of 2.
      * Marks off multiples starting at p*p with step = 2*p (only odd steps),
        taking advantage of slice assignment for bulk updates.

    Parameters
    ----------
    n: int
        Upper bound inclusive. Must be non‑negative; values < 2 yield [].

    Returns
    -------
    List[int]
        All primes <= n in ascending order.
    """
    if n < 2:
        return []

    # Bytearray where index i == 1 means "i is potentially prime"
    # Initially assume all numbers are prime (1), then clear composites.
    is_prime = bytearray(b'\x01') * (n + 1)
    # 0 and 1 are not prime
    is_prime[0:2] = b'\x00\x00'

    # Special case: mark all even numbers > 2 as composite.
    # We keep the entry for 2 (prime) untouched.
    if n >= 4:
        # Slice assignment: start at 4, step of 2 => all even indices beyond 2
        is_prime[4:n + 1:2] = b'\x00' * ((n - 4) // 2 + 1)

    limit = isqrt(n)
    # Iterate over odd candidates only (3,5,7,...)
    for p in range(3, limit + 1, 2):
        if is_prime[p]:
            # Start striking out at p*p; step of 2*p skips even multiples.
            start = p * p
            if start > n:
                break
            step = p << 1  # same as 2 * p
            # Compute how many elements we need to clear
            count = (n - start) // step + 1
            # Use slice assignment with a bytes object filled with zeros.
            is_prime[start:n + 1:step] = b'\x00' * count

    # Collect all indices that remain marked as prime.
    return [i for i, flag in enumerate(is_prime) if flag]


# ------------------------------------------------------------------------
# Simple sanity‑check when the module is executed directly.
# This block is not required by the core API but aids quick debugging.
if __name__ == "__main__":
    # Test edge cases
    assert primes_up_to(0) == []
    assert primes_up_to(1) == []

    # Small known output
    expected_small = [2, 3, 5, 7]
    assert primes_up_to(10) == expected_small

    # Quick performance peek for n=2_000_000 (should finish well under a second)
    import time
    t0 = time.time()
    _ = primes_up_to(2_000_000)
    elapsed = time.time() - t0
    print(f"Computed primes up to 2,000,000 in {elapsed:.3f}s; count={len(_)}")