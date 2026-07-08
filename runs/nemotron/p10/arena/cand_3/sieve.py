"""Fast Sieve of Eratosthenes using bytearray with odd-only indexing and slice assignment."""

def primes_up_to(n: int) -> list[int]:
    """Return sorted list of all primes <= n using optimized odd-only sieve.

    Args:
        n: Upper bound (inclusive). For n < 2, returns empty list.

    Returns:
        List of primes <= n in ascending order.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]

    # Odd-only sieve: index i represents number 2*i + 3
    # Size covers odd numbers from 3 to n inclusive
    size = (n - 3) // 2 + 1
    sieve = bytearray(b'\x01') * size  # 1 = prime candidate, 0 = composite

    limit = int(n**0.5)
    # Only need limit)5)
    # Max index to check: corresponds to sqrt(n)
    max_i = (limit - 3) // 2

    for i in range(max_i + 1):
        if sieve[i]:
            p = 2 * i + 3
            # Start crossing off at p*p, which has index (p*p - 3) // 2
            start = (p * p - 3) // 2
            # Step is p (since we skip evens, step in index space is p)
            sieve[start::p] = b'\x00' * ((size - start - 1) // p + 1)

    # Collect primes: 2 + all odd primes from sieve
    primes = [2]
    primes.extend(2 * i + 3 for i, is_prime in enumerate(sieve) if is_prime)
    return primes


if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 2_000_000

    start = time.perf_counter()
    primes = primes_up_to(n)
    elapsed = time.perf_counter() - start

    print(f"primes_up_to({n}) = {len(primes)} primes in {elapsed:.4f}s")
    if n <= 100:
        print(primes)