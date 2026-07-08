#!/usr/bin/env python3
"""
Fast implementation of Sieve of Eratosthenes.
Uses bytearray, skips even numbers, and employs slice assignments for efficiency.
Returns sorted list of primes up to n (inclusive).
"""

def primes_up_to(n):
    """Return sorted list of primes <= n using Sieve of Eratosthenes."""
    if n < 2:
        return []
    if n == 2:
        return [2]
    
    # Initialize sieve, skipping even numbers
    sieve = bytearray([1]) * ((n + 1) // 2)
    sieve[0] = 0  # Mark 1 as non-prime
    
    # Sieve of Eratosthenes
    for i in range(1, int(len(sieve) ** 0.5) + 1):
        if sieve[i]:
            # Mark multiples starting from i*(i+1) to skip even multiples
            step = 2 * i + 1
            start = step * i
            end = len(sieve)
            sieve[start:end:step] = b'\x00' * len(sieve[start:end:step])
    
    # Build result list: 2 plus all odd numbers marked as prime
    primes = [2]
    primes.extend([2 * i + 1 for i in range(1, len(sieve)) if sieve[i]])
    return primes
