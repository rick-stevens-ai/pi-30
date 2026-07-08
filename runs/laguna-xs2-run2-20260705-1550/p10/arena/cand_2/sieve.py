"""Optimized Sieve of Eratosthenes for primes_up_to(n)."""


def primes_up_to(n: int) -> list[int]:
    """Return sorted list of all primes <= n.

    Uses bytearray for memory efficiency, skips even numbers,
    and uses slice assignment for fast marking.

    Args:
        n: Upper bound (inclusive)

    Returns:
        Sorted list of primes <= n, or empty list for n < 2
    """
    if n < 2:
        return []

    # 2 is the only even prime
    if n == 2:
        return [2]

    # Sieve for odd numbers only: index i represents number 2*i+3
    # So we need primes up to n, which means odd numbers up to n
    # Count of odd numbers from 3 to n (inclusive)
    size = (n - 1) // 2  # number of odd values >= 3 and <= n
    sieve = bytearray(b'\x01') * size  # True = prime candidate

    # For each odd i starting from 3, if sieve[i//2] is True,
    # mark its odd multiples as composite
    # i = 2*k + 3, start marking from i*i
    # i*i = (2k+3)^2 = 4k^2 + 12k + 9
    # For odd multiples: i*i, i*i + 2i, i*i + 4i, ...
    # In terms of odd index: (i*i - 3)//2, ((i*i - 3)//2) + i, ...

    limit = int(n ** 0.5)
    for k in range((limit - 1) // 2):
        if sieve[k]:
            i = 2 * k + 3  # the odd prime
            # First odd multiple >= i*i
            start = (i * i - 3) // 2
            # Step by i (since i is odd, i*i, i*i+2i, i*i+4i, ... are odd multiples)
            sieve[start::i] = b'\x00' * ((size - start + i - 1) // i)

    # Build result: 2 followed by odd primes
    primes = [2]
    primes.extend(2 * k + 3 for k in range(size) if sieve[k])
    return primes