# P23 SEED: trial division for every number. Correct but slow.
def count_primes(n):
    if n <= 2: return 0
    if n == 3: return 1
    size = n // 2
    sieve = bytearray([1]) * size
    sieve[0] = 0
    limit = int(((n - 1)**0.5 - 1) / 2)
    for i in range(1, limit + 1):
        p = 2 * i + 1
        if sieve[i]:
            start = (p * p - 1) // 2
            sieve[start::p] = bytearray(len(range(start, size, p)))
    return sum(sieve) + 1
