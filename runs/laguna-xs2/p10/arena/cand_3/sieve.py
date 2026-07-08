"""Optimized Sieve of Eratosthenes using bytearray and slice assignment."""


def primes_up_to(n):
    """Return sorted list of primes <= n.
    
    Uses bytearray for memory efficiency and slice assignment for speed.
    Handles n < 2 as empty list. Optimized for n=2,000,000.
    
    >>> primes_up_to(10)
    [2, 3, 5, 7]
    >>> primes_up_to(1)
    []
    >>> primes_up_to(2)
    [2]
    """
    if n < 2:
        return []
    if n == 2:
        return [2]
    
    # For n >= 3, work with odd numbers only
    # Index i represents number 2*i + 3
    size = (n - 1) // 2
    sieve = bytearray(b'\x01') * size  # True = might be prime
    
    # Mark composites using slice assignment
    for i in range(size):
        p = 2 * i + 3
        if p * p > n:
            break
        if sieve[i]:  # p is prime
            start = (p * p - 3) // 2
            sieve[start::p] = b'\x00' * ((size - start - 1) // p + 1)
    
    return [2] + [2 * i + 3 for i in range(size) if sieve[i]]