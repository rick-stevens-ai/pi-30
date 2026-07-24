def primes_up_to(n):
    if n < 2:
        return []
    if n == 2:
        return [2]
    size = (n - 1) // 2
    sieve = bytearray(b'\x01') * size
    import math
    limit = int(math.isqrt(n))
    for i in range(1, limit // 2 + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = i + p * (p - 1) // 2
            sieve[start::p] = b'\x00' * max(0, (size - 1 - start) // p + 1)
    return [2] + [2 * i + 1 for i in range(1, size + 1) if sieve[i]]
