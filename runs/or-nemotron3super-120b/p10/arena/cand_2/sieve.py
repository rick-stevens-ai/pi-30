def sieve(n: int):
    """Return list of primes <= n using sieve of Eratosthenes."""
    if n < 2:
        return []
    if n == 2:
        return [2]
    # n >= 3
    size = (n - 1) // 2  # number of odd numbers <= n
    sieve = bytearray(b'\x01') * size
    # sieve[i] corresponds to number 2*i+3
    limit = int(n**0.5)
    for i in range((limit - 3) // 2 + 1):
        if sieve[i]:
            p = 2 * i + 3
            start = (p * p - 3) // 2
            sieve[start::p] = b'\x00' * ((size - start - 1) // p + 1)
    # collect primes
    primes = [2]
    primes.extend(2 * i + 3 for i, is_prime in enumerate(sieve) if is_prime)
    return primes

if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(sieve(n))
