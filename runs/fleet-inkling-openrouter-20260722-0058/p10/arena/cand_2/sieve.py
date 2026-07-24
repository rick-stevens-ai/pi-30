"""Fast Sieve of Eratosthenes using bytearray, odd-only, slice assign."""

def primes_up_to(n):
    if n < 2:
        return []
    if n == 2:
        return [2]
    # bytearray: 1 = prime, 0 = composite. Index = number.
    # Only odd numbers > 1 are tracked; index i represents 2*i+1.
    size = (n - 1) // 2
    sieve = bytearray(b'\x01') * size
    sieve[0] = 0  # 3? Wait: index 0 -> 1? Let's keep direct 0..n representation for simplicity.
    # Actually direct mapping is faster for slice assignment and clarity:
    sieve = bytearray(b'\x01') * (n + 1)
    sieve[0:2] = b'\x00\x00'
    limit = int(n ** 0.5) + 1
    for p in range(2, limit):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:n+1:step] = b'\x00' * ((n - start)//step + 1)
    return [i for i, is_prime in enumerate(sieve) if is_prime]
