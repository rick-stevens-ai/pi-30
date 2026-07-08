# P23 SEED: trial division for every number. Correct but slow.
def count_primes(n):
    # Sieve of Eratosthenes with bytearray, skipping evens.
    if n <= 2:
        return 0
    primes = bytearray(b'\x01') * (n)
    primes[0] = 0
    primes[1] = 0
    limit = int(n ** 0.5) + 1
    for i in range(2, limit):
        if primes[i]:
            step = i
            start = i * i
            for j in range(start, n, step):
                primes[j] = 0
    return sum(primes[:n])
