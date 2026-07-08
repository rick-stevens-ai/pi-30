# P23 SEED: trial division for every number. Correct but slow.
def count_primes(n):
    if n <= 2:
        return 0
    sieve = bytearray([1]) * ((n) // 2)
    sieve[0] = 0
    for i in range(1, int(n**0.5) // 2 + 1):
        if sieve[i]:
            prime = 2 * i + 1
            start = prime * prime // 2
            sieve[start::prime] = b'\x00' * len(sieve[start::prime])
    count = sum(sieve)
    if n > 2:
        count += 1  # for the prime number 2
    return count
