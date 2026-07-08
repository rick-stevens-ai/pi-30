# P23: Sieve of Eratosthenes with bytearray, skipping evens.
def count_primes(n):
    if n < 3:
        return 0
    # Only track odd numbers >= 3: index i represents value 2*i+3.
    size = n // 2 - 1  # count of odd values in [3, n)
    if size < 0:
        size = 0
    sieve = bytearray([1]) * size
    # value v = 2*i+3, mark odd composites starting at v*v.
    i = 0
    v = 3
    while v * v < n:
        if sieve[i]:
            start = v * v
            # start is odd; odd multiples of v differ by 2v -> v indices.
            start_idx = (start - 3) // 2
            sieve[start_idx:size: v] = bytearray(len(sieve[start_idx:size: v]))
        i += 1
        v += 2
    # 2 is prime, plus the odd primes still marked in sieve
    return 1 + sum(sieve)
