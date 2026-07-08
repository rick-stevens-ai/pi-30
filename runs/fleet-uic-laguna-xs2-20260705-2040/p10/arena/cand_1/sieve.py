"""Optimized Sieve of Eratosthenes for primes_up_to(n)."""

import math


def primes_up_to(n: int) -> list[int]:
    """Return sorted list of primes <= n.

    Uses bytearray for memory efficiency, skips even numbers,
    and uses slice assignment for speed.

    Args:
        n: Upper bound (inclusive)

    Returns:
        Sorted list of primes <= n, empty if n < 2
    """
    # Edge cases
    if n < 2:
        return []

    # 2 is the only even prime
    if n == 2:
        return [2]

    # Sieve for odd numbers only: index i represents number 2*i + 3
    # So we only need (n - 1) // 2 numbers to check
    sqrt_n = int(math.isqrt(n))
    size = (n - 1) // 2  # count of odd numbers >= 3 and <= n
    sieve = bytearray(b'\x01') * size  # True = possibly prime

    # Mark composites
    for i in range(size):
        p = 2 * i + 3
        if p > sqrt_n:
            break
        if sieve[i]:  # p is prime
            # Start at p^2, which is odd. Index of p^2: (p^2 - 3) // 2
            # Step by 2p to skip even multiples
            start = (p * p - 3) // 2
            step = p
            sieve[start::step] = b'\x00' * ((size - start + step - 1) // step)

    # Build result: 2 followed by odd primes
    primes = [2]
    primes.extend(2 * i + 3 for i in range(size) if sieve[i])
    return primes