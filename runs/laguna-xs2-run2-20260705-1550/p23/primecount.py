# P23: Sieve of Eratosthenes with bytearray, skip evens.
def count_primes(n):
    if n < 3: return 0
    count = 1  # 2 is prime
    size = max(0, (n - 2) // 2)
    sieve = bytearray([1]) * size
    for i in range(size):
        if sieve[i]:
            p = 2 * i + 3
            if p * p >= n:
                break
            start = (p * p - 3) // 2
            sieve[start::p] = bytearray(len(sieve[start::p]))
    return count + sum(sieve)
