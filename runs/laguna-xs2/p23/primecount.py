# P23: Sieve of Eratosthenes with bytearray, skip evens.
def count_primes(n):
    if n < 3:
        return 0
    # count 2, then sieve odd numbers starting from 3
    count = 1
    # sieve[i] represents number 2*i + 3
    size = (n - 3) // 2 + 1
    sieve = bytearray([1]) * size
    for i in range(size):
        p = 2 * i + 3
        if p * p >= n:
            break
        if sieve[i]:
            count += 1
            # mark odd multiples of p starting from p*p
            start = (p * p - 3) // 2
            sieve[start::p] = bytearray(len(sieve[start::p]))
    # count remaining primes >= sqrt(n) and < n
    for j in range(i, size):
        if sieve[j] and 2 * j + 3 < n:
            count += 1
    return count
