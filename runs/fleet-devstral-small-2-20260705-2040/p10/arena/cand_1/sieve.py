"""
Sieve of Eratosthenes implementation.

Exposes:
- primes_up_to(n): returns sorted list of primes <= n
"""

def primes_up_to(n):
    """Return sorted list of primes <= n.
    
    Uses Sieve of Eratosthenes with optimizations:
    - bytearray for bit-packed sieve
    - skip even numbers (except 2)
    - slice assignment for marking multiples
    
    Correct for n < 2 (returns empty list).
    """
    if n < 2:
        return []
    
    # Special case: n == 2
    if n == 2:
        return [2]
    
    # Sieve size: (n + 1) // 2 to cover odd numbers up to n
    size = (n + 1) // 2
    sieve = bytearray([1]) * size
    
    # 1 is not prime
    sieve[0] = 0
    
    # Mark multiples of odd primes starting from 3
    for i in range(1, int(n ** 0.5) // 2 + 1):
        if sieve[i]:
            # Prime = 2*i + 1
            prime = 2 * i + 1
            # Start marking from prime^2, step 2*prime (skip evens)
            start = prime * prime
            # Convert start to index: (start - 1) // 2
            sieve[(start - 1) // 2 :: prime] = b"\x00" * len(sieve[(start - 1) // 2 :: prime])
    
    # Collect primes: 2 + [2*i + 1 for i where sieve[i] == 1]
    primes = [2]
    primes.extend(2 * i + 1 for i in range(1, size) if sieve[i])
    return primes
