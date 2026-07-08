# P23 SEED: trial division for every number. Correct but slow.
def count_primes(n):
    # Fast Sieve of Eratosthenes using a bytearray and skipping even numbers.
    if n <= 2:
        return 0
    sieve = bytearray(b'\x01') * n
    # 0 and 1 are not prime
    sieve[0:2] = b'\x00\x00'
    # Mark even numbers >2 as non‑prime
    if n > 4:
        sieve[4:n:2] = b'\x00' * ((n - 4 + 1) // 2)
    limit = int(n ** 0.5) + 1
    for p in range(3, limit, 2):
        if sieve[p]:
            start = p * p
            step = p * 2  # skip even multiples
            sieve[start:n:step] = b'\x00' * ((n - start - 1) // step + 1)
    return sum(sieve)
