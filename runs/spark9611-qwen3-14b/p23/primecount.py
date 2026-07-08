# P23 SEED: trial division for every number. Correct but slow.
def count_primes(n):
    if n < 2:
        return 0
    sieve = bytearray([1]) * n
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i : n+1 : i] = b'\x00' * len(sieve[i*i : n+1 : i])
    return sum(sieve)
