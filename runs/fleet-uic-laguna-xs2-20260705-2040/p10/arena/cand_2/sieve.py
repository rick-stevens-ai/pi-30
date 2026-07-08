"""
Optimized Sieve of Eratosthenes for finding all primes up to n.

Uses bytearray for memory efficiency, skips even numbers (except 2),
and employs slice assignment for fast composite marking.
"""

import math


def primes_up_to(n):
    """
    Return sorted list of all primes <= n.
    
    Args:
        n: Upper bound (inclusive)
        
    Returns:
        Sorted list of primes <= n. Empty list for n < 2.
        
    Examples:
        >>> primes_up_to(10)
        [2, 3, 5, 7]
        >>> primes_up_to(1)
        []
        >>> primes_up_to(2)
        [2]
    """
    if n < 2:
        return []
    
    # Handle the only even prime
    if n == 2:
        return [2]
    
    # Sieve for odd numbers >= 3
    # Index i represents number 2*i + 3
    # Index 0 = 3, index 1 = 5, index 2 = 7, etc.
    size = (n - 1) // 2
    sieve = bytearray(size)  # 0 = prime candidate, 1 = composite
    
    limit = int(math.isqrt(n))
    
    for i in range(size):
        p = 2 * i + 3
        if p > limit:
            break
        if sieve[i] == 0:  # p is prime
            # Mark all odd multiples of p starting from p*p
            start = (p * p - 3) // 2
            sieve[start::p] = b'\x01' * ((size - start + p - 1) // p)
    
    # Build result: 2 followed by remaining primes
    primes = [2]
    primes.extend(2 * i + 3 for i in range(size) if sieve[i] == 0)
    return primes


if __name__ == "__main__":
    # Quick verification
    print(primes_up_to(30))
    print(len(primes_up_to(2000000)))  # Count primes up to 2M