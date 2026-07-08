"""
Generate primes up to n efficiently using the Sieve of Eratosthenes.

Algorithm characteristics:
- Skips all even numbers (except 2)
- Uses bytearray for O(n) space
- Slices for efficient marking
- Returns sorted list of primes
"""

def primes_up_to(n):
    """Return sorted list of primes <= n."""
    if n < 2:
        return []
    
    # Only store odd numbers >= 3
    # Index k in sieve represents number 2k + 3
    size = max(0, (n - 3) // 2)
    sieve = bytearray([1]) * (size + 1)
    
    # 3, 5, 7 are the first candidates
    # Square root of n as integer
    sqrt_n = int(n ** 0.5) + 1
    
    for i in range(1, sqrt_n // 2 + 1):
        if sieve[i]:
            prime = 2 * i + 3
            # Start marking from prime^2, step 2*prime (only odd multiples)
            start = (prime * prime - 3) // 2
            sieve[start::prime] = b"\x00" * len(sieve[start::prime])
    
    # Collect primes: 2 plus odds that remain marked
    primes = [2]
    primes.extend(2 * i + 3 for i in range(size + 1) if sieve[i] and (2 * i + 3) <= n)
    return primes
