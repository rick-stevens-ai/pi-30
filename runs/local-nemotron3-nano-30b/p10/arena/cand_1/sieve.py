import math

def primes_up_to(n: int) -> list[int]:
    """
    Return a sorted list of all prime numbers <= n.
    Works for n < 2 (returns []), includes 2, and uses an optimized
    bytearray sieve that skips even numbers. Suitable for n up to at
    least 2_000_000 using only the Python standard library.
    """
    if n < 2:
        return []

    # Start with prime 2 if needed
    primes = [2] if n >= 2 else []

    # Number of odd candidates >=3 and <=n
    size = (n - 1) // 2   # how many odd numbers from 3 up to n inclusive
    sieve = bytearray(b'\x01') * size   # True == potential prime

    limit = int(math.isqrt(n))
    max_i = (limit - 3) // 2            # Largest i where p=2*i+3 <= limit
    for i in range(max_i + 1):
        if sieve[i]:
            p = 2 * i + 3               # actual prime number
            # First multiple to strike is p*p, which is odd.
            start_idx = (p * p - 3) // 2   # its index in the sieve array
            if start_idx >= size:
                continue                  # nothing to mark
            # Number of elements to clear: ceil((size-1-start_idx)/p)
            count = (size - 1 - start_idx + p) // p
            sieve[start_idx::p] = b'\x00' * count

    # Convert remaining True entries back to primes
    primes.extend([2 * i + 3 for i, is_prime in enumerate(sieve) if is_prime])
    return primes