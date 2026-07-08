# P23 SEED: trial division for every number. Correct but slow.
def count_primes(n):
    # Sieve of Eratosthenes using bytearray, skipping even numbers
    if n <= 2:
        return 0
    # only consider odd numbers: index i represents number 2*i+1
    size = n // 2
    sieve = bytearray(b'\x01') * size
    sieve[0] = 0  # 1 is not prime
    limit = int(n ** 0.5)
    for p in range(3, limit + 1, 2):
        if sieve[p // 2]:
            start = p * p
            step = p
            sieve[start // 2 :: step] = b'\x00' * ((size - start // 2 - 1) // step + 1)
    # count primes: include 2 if within range, plus odd primes
    count = 1 if n > 2 else 0
    count += sum(sieve[1:])  # exclude index 0 (number 1)
    return count
