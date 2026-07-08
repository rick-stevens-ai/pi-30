def count_primes(n):
    """Return the number of primes strictly less than n."""
    if n < 3:
        return 0
    # sieve for odd numbers only: index i represents number 2*i+1
    size = n // 2
    sieve = bytearray(b'\x01') * size
    sieve[0] = 0  # 1 is not prime
    limit = int(n ** 0.5)
    # only need to check odd factors up to sqrt(n)
    # i corresponds to p = 2*i+1
    for i in range(1, (limit // 2) + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p) // 2
            step = p
            sieve[start::step] = b'\x00' * ((size - start - 1) // step + 1)
    # count odd primes (excluding 2) plus the prime 2
    return sum(sieve) + 1