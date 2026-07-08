# Optimized prime counting using a bytearray Sieve of Eratosthenes (skipping evens).

def count_primes(n):
    """Return the number of prime numbers less than *n*.
    Uses a memory‑efficient sieve that stores only odd numbers.
    """
    if n <= 2:
        return 0
    # Number of odd numbers < n (1,3,5,...)
    size = n // 2
    sieve = bytearray(b'\x01') * size
    # 1 is not prime (odd index 0 corresponds to number 1)
    sieve[0] = 0
    limit = int(n ** 0.5)
    # Iterate over odd candidates up to sqrt(n)
    for i in range(1, (limit // 2) + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p) // 2
            sieve[start::p] = b'\x00' * ((size - start - 1) // p + 1)
    # Count primes: include 2 plus odd primes marked by the sieve
    return 1 + sum(sieve)

