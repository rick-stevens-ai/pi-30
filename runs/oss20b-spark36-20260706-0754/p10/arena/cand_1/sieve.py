"""
Simple, fast Sieve of Eratosthenes.

Provides a single function ``primes_up_to(n)`` returning a sorted list of all prime numbers <= n.

The implementation uses a bytearray to represent only the odd numbers up to n. Even numbers are omitted except for 2. This cuts memory usage roughly in half and speeds up marking composites via slice assignment.

The algorithm is suitable for moderate sizes (e.g., n≈2 000 000) with negligible overhead by leveraging efficient memory operations in CPython.

---

Design details:

* ``n < 2`` → return an empty list.
* If ``n == 2`` → ``[2]``.
* For larger `n`, we work modulo the mapping
  
  ``index i`` ↔ number ``2*i + 1`` (odd numbers).
  The sieve length is ``m = n//2 + 1``; ``is_prime[i]`` indicates primality of ``2*i+1``.
* The standard Sieve marks composites starting at the square of each discovered prime.
  In terms of indices the first composite index is ``(p*p)//2`` where ``p = 2*i+1``.

Slice assignment is used for bulk zeroing which gives a measurable speedup over explicit loops.
"""

from __future__ import annotations

from typing import List

__all__: list[str] = ["primes_up_to"]


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of all prime numbers <= ``n``.

    Parameters
    ----------
    n:
        Upper bound (inclusive). ``n`` may be negative; in that case an empty list is returned.

    Returns
    -------
    List[int]
        List of primes in ascending order. The result is never a generator or lazy.

    Performance notes
    -----------------
    * Uses a :class:`bytearray` to store the sieve for odd numbers only.
    * Slice assignment zeroes composite indices at once, which is faster than
      individual assignments inside loops.
    * For ``n = 2_000_000`` the function completes well under a second on typical hardware.

    Examples
    --------
    >>> primes_up_to(10)
    [2, 3, 5, 7]
    >>> primes_up_to(1) == []
    True
    >>> primes_up_to(2)
    [2]
    """

    if n < 2:
        return []
    # Handle the trivial small cases first – keeps logic tidy for later.
    if n == 2:
        return [2]

    # ``m`` is the number of odd integers up to and including ``n``. It also defines
    # the length of our sieve bytearray.
    m = (n + 1) // 2  # number of odd integers <= n
    sieve: bytearray = bytearray(1) * m
    sieve[0] = 0  # 1 is not prime.

    import math
    limit = (math.isqrt(n) - 1) // 2
    for i in range(1, limit + 1):
        if sieve[i]:
            p: int = 2 * i + 1
            start_idx: int = (p * p) // 2
            step: int = p
            if start_idx < len(sieve):
                sieve[start_idx::step] = b"\x00" * ((len(sieve) - start_idx + step - 1) // step)

    primes: list[int] = [2]
    # Convert odd indices back to their corresponding prime numbers.
    primes.extend([2 * i + 1 for i in range(1, m) if sieve[i]])
    return primes

# Optional demonstration when run as a script – not executed during imports.
if __name__ == "__main__":
    import sys

    try:
        bound: int = int(sys.argv[1])
    except (IndexError, ValueError):
        bound = 100
    print(f"Primes up to {bound}:", primes_up_to(bound))
