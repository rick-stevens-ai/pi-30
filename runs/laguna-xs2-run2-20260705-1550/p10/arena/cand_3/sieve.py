"""Optimized Sieve of Eratosthenes for primes_up_to(n)."""

def primes_up_to(n: int) -> list[int]:
    """Return sorted list of primes <= n."""
    if n < 2:
        return []
    
    # 2 is the only even prime
    if n == 2:
        return [2]
    
    # Sieve odd numbers only: index i represents 2*i+3
    # So we need (n - 1) // 2 odd candidates from 3 to n
    size = (n - 1) // 2
    sieve = bytearray(size)  # 0 means prime, 1 means composite
    
    # Only need to check up to sqrt(n)
    limit = int(n ** 0.5)
    
    for i, is_prime in enumerate(sieve):
        p = 2 * i + 3
        if p > limit:
            break
        if is_prime == 0:  # p is prime
            # Mark odd multiples of p starting from p*p
            # p*p is odd, and we step by 2*p (next odd multiple)
            start = (p * p - 3) // 2
            step = p
            sieve[start::step] = b'\x01' * ((size - start + step - 1) // step)
    
    # Build result: start with 2, then odd primes
    return [2] + [2 * i + 3 for i in range(size) if sieve[i] == 0]