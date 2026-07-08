from array import array

def count_primes(n):
    if n < 2:
        return 0
    # Sieve of Eratosthenes using bytearray for efficiency, counting primes < n
    sieve = bytearray([1]) * (n // 1)
    sieve[0] = sieve[1] = 0
    lim = int(n ** 0.5) + 1
    for i in range(2, lim):
        if sieve[i]:
            # Slice assignment is faster than loop for marking multiples
            start = i * i
            step = i
            end = n
            sieve[start:end:step] = b'\x00' * len(sieve[start:end:step])
    return sum(sieve)
