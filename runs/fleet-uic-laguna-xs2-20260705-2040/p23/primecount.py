# P23: Sieve of Eratosthenes with bytearray, skipping evens.
def count_primes(n):
    if n < 3: return 0
    # sieve[i] represents odd number 2*i + 3
    size = 0 if n <= 3 else (n - 2) // 2
    sieve = bytearray([1]) * size
    for i in range(size):
        p = 2 * i + 3
        if p * p >= n:
            break
        if sieve[i]:
            # mark odd multiples of p starting from p*p
            start = (p * p - 3) // 2
            step = p
            sieve[start::step] = bytearray(len(sieve[start::step]))
    return 1 + sum(sieve)  # 1 for the prime 2, plus count of odd primes