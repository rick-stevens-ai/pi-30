# P23: Sieve of Eratosthenes over odd numbers only (bytearray), skip evens.
def count_primes(n):
    if n < 3:
        return 0
    # 2 is the only even prime; sieve the odd numbers 3,5,7,...
    # sieve[i] represents the odd number 2*i + 3
    size = n // 2 - 1
    sieve = bytearray([1]) * size
    i = 0
    # only sieve with primes p where p*p < n  (p = 2*i + 3)
    while (2 * i + 3) ** 2 < n:
        if sieve[i]:
            p = 2 * i + 3
            start = (p * p - 3) // 2
            sieve[start::p] = bytearray(len(sieve[start::p]))
        i += 1
    return 1 + sum(sieve)  # +1 for the prime 2