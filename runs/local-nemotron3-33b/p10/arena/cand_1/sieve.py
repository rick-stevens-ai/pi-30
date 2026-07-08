"""sieve.py - Sieve of Eratosthenes implementation that returns sorted primes <= n.

Uses a bytearray for speed and skips even numbers after handling 2, making it fast up to n = 2_000_000 while staying within the Python standard library.
"""

import math

def primes_up_to(n: int):
    """Return a sorted list of all prime numbers <= n.

    - For n < 2 returns an empty list (edge case).
    - Uses a bytearray where each index indicates primality.
    - Skips even numbers except 2 to improve speed and memory usage.
    """
    if n < 2:
        return []

    # Allocate sieve; one byte per integer
    sieve = bytearray(b'\x01') * (n + 1)
    sieve[0] = sieve[1] = 0  # 0 and 1 are not prime

    # Remove even numbers > 2 in bulk.
    if n >= 4:
        sieve[4:n+1:2] = b'\x00' * (((n - 4) // 2) + 1)

    limit = int(math.isqrt(n))  # sqrt(n) is sufficient as an upper bound

    for i in range(3, limit + 1, 2):  # iterate only odd numbers
        if sieve[i]:
            start = i * i          # first multiple of i that needs clearing
            step = i * 2           # skip even multiples (odd step)
            count = (n - start) // step + 1
            sieve[start:n+1:step] = b'\x00' * count

    primes = [2]
    for i in range(3, n+1, 2):   # collect remaining odd primes
        if sieve[i]:
            primes.append(i)
    return primes

# Simple command‑line demo
if __name__ == "__main__":
    import sys
    try:
        test_n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    except ValueError:
        print("Usage: python sieve.py <non-negative integer>")
        sys.exit(1)

    result = primes_up_to(test_n)
    print(f"Primes up to {test_n}:")
    print(result)