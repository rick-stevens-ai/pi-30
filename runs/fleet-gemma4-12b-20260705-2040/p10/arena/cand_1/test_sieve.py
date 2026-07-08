def primes_up_to(n):
    if n < 2:
        return []
    if n == 2:
        return [2]
    limit = n // 2 + 1
    sieve = bytearray([1]) * limit
    sieve[0] = 0
    for i in range(1, int(n**0.5) // 2 + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p - 1) // 2
            sieve[start::p] = bytes([0]) * ((limit - 1 - start) // p + 1)
    primes = [2]
    for i in range(1, limit):
        if sieve[i]:
            primes.append(2 * i + 1)
    return [p for p in primes if p <= n]

print(primes_up_to(6))
