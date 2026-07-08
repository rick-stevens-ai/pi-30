"""Optimized Sieve of Eratosthenes for primes_up_to(n)."""


def primes_up_to(n: int) -> list[int]:
    """Return sorted list of all primes <= n.

    Uses bytearray and skip-evens optimization for speed at n=2,000,000+.
    """
    if n < 2:
        return []

    # 2 is the only even prime; work with odd numbers only
    # index i represents number 2*i + 3
    size = (n - 1) // 2
    is_prime = bytearray(b'\x01') * size  # all odd candidates start as prime

    # Sieve: mark composites
    limit = int(n**0.5)
    for i, is_p in enumerate(is_prime):
        p = 2 * i + 3
        if p > limit:
            break
        if is_p:
            # Start at p^2, step 2p (skip even multiples)
            start = (p * p - 3) // 2
            is_prime[start::p] = b'\x00' * ((size - start + p - 1) // p)

    # Build result: 2 followed by remaining odd primes
    return [2] + [2 * i + 3 for i, v in enumerate(is_prime) if v]