"""Sieve of Eratosthenes optimized for speed at n=2,000,000.

Uses bytearray (1 byte per odd number), skips evens entirely,
and uses slice assignment for fast composite marking.
"""

def primes_up_to(n: int) -> list[int]:
    """Return sorted list of all primes <= n.

    Args:
        n: Upper bound (inclusive).

    Returns:
        List of primes in ascending order. Empty for n < 2.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]

    # Only represent odd numbers: index i -> number 2*i + 3
    # Size needed: odds from 3 to n inclusive
    size = (n - 3) // 2 + 1  # count of odd numbers 3,5,7,... <= n
    sieve = bytearray(b'\x01') * size  # 1 = potentially prime

    limit = int(n**0.5)
    # Only need to sieve up to sqrt(n)
    # p = 2*i + 3, so i = (p - 3) // 2
    for i in range((limit - 3) // 2 + 1):
        if sieve[i]:
            p = 2 * i + 3
            # Start crossing off at p*p, which corresponds to index:
            # p*p = (2*i+3)^2 = 4*i^2 + 12*i + 9
            # Index of p*p = (p*p - 3) // 2 = 2*i^2 + 6*i + 3
            start = 2 * i * i + 6 * i + 3
            # Step is p (since we skip evens, step in index-space is p)
            sieve[start::p] = b'\x00' * ((size - start - 1) // p + 1)

    # Build result: 2 plus all odd numbers where sieve[i] == 1
    primes = [2]
    primes.extend(2 * i + 3 for i, is_prime in enumerate(sieve) if is_prime)
    return primes


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    primes = primes_up_to(n)
    print(f"pi({n}) = {len(primes)}")
    if n <= 100:
        print(primes)