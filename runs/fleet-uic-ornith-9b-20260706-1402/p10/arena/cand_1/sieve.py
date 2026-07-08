def primes_up_to(n: int) -> list[int]:
    if n < 2:
        return []

    # Sieve of Eratosthenes on odd numbers only, encoded in a bytearray.
    # Index i represents the candidate number (i << 1 | 1).
    limit = (n - 1) // 2 + 1
    sieve = bytearray(b'\x01') * limit

    for p in range(3, int(n**0.5) + 1, 2):
        base = p * p >> 1           # (p*p - 1) // 2: start offset in odd-only array
        sieve[base::p] = b'\x00' * len(sieve[base::p])

    odds = [(i << 1) | 1 for i in range(1, limit) if sieve[i]]
    return [2] + odds if n >= 2 else []
