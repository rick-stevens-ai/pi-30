def count_primes(n):
    if n < 2:
        return 0
    sieve = bytearray(b'\x01') * n
    sieve[0] = sieve[1] = 0
    if n > 2:
        sieve[4:n:2] = b'\x00' * ((n - 4 - 1) // 2 + 1)
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i]:
            sieve[i*i:n:i*2] = b'\x00' * ((n - i*i - 1) // (i*2) + 1)
    return sum(sieve)
