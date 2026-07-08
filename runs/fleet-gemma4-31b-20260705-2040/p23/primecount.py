# P23 SEED: trial division for every number. Correct but slow.
def count_primes(n):
    if n <= 2: return 0
    sieve = bytearray([1]) * (n // 2)
    sieve[0] = 0
    for i in range(1, int(n**0.5)//2 + 1):
        if sieve[i]:
            p = 2*i + 1
            start = (p*p - 1) // 2
            if start < len(sieve):
                sieve[start::p] = b'\x00' * len(range(start, len(sieve), p))
    return sum(sieve) + 1
