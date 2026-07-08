def primes_up_to(n):
    """
    Returns a sorted list of all prime numbers up to and including n.
    Uses an optimized Sieve of Eratosthenes with bytearray, odd-only 
    indexing, and slice assignment for performance.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]

    # We only store primality for odd numbers starting from 1.
    # Index i represents the number 2*i + 1.
    # The largest odd number <= n is (n if n%2 else n-1).
    # Its index is ((n - 1) // 2).
    size = (n - 1) // 2 + 1
    sieve = bytearray([1]) * size
    sieve[0] = 0  # 1 is not prime

    # The maximum value of p we need to sieve is sqrt(n).
    # Let v = 2*i + 1. We stop when v*v > n.
    limit = int(n**0.5)
    for i in range(1, (limit - 1) // 2 + 1):
        if sieve[i]:
            p = 2 * i + 1
            # The first odd multiple of p to mark is p*p.
            # Index of p*p: (p*p - 1) // 2.
            start = (p * p - 1) // 2
            # Every subsequent odd multiple of p occurs every p indices.
            # e.g., for p=3, we mark 9, 15, 21... indices are 4, 7, 10...
            sieve[start::p] = b'\x00' * ((size - 1 - start) // p + 1)

    # Collect primes: always include 2, then all odd numbers where sieve[i] is True.
    return [2] + [2 * i + 1 for i in range(1, size) if sieve[i]]

if __name__ == "__main__":
    import sys
    import time

    # Basic tests
    test_cases = {
        -1: [],
        0: [],
        1: [],
        2: [2],
        3: [2, 3],
        10: [2, 3, 5, 7],
        20: [2, 3, 5, 7, 11, 13, 17, 19],
    }

    for n, expected in test_cases.items():
        result = primes_up_to(n)
        assert result == expected, f"Failed for n={n}: expected {expected}, got {result}"

    # Performance test for n=2,000,000
    N = 2_000_000
    start_time = time.perf_counter()
    primes = primes_up_to(N)
    end_time = time.perf_counter()

    print(f"Found {len(primes)} primes up to {N:,} in {end_time - start_time:.4f} seconds.")
    # The number of primes up to 2,000,000 is known to be 148,933.
    assert len(primes) == 148933, f"Incorrect count for N=2M: {len(primes)}"
