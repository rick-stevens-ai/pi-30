"""Optimized Sieve of Eratosthenes for primes_up_to(n)."""

def primes_up_to(n: int) -> list[int]:
    """Return sorted list of all primes <= n.
    
    Uses bytearray for memory efficiency, skips even numbers,
    and uses slice assignment for fast marking.
    """
    if n < 2:
        return []
    
    # 2 is the only even prime; handle separately
    if n == 2:
        return [2]
    
    # Only consider odd numbers: 3, 5, 7, ..., n
    # Index i maps to number 2*i + 3
    size = (n - 3) // 2 + 1
    is_prime = bytearray(b'\x01') * size  # True for all odds initially
    
    # Check odd factors up to sqrt(n)
    limit = int(n**0.5)
    
    # Iterate over odd primes p where p <= sqrt(n)
    # p = 2*i + 3, so i = (p - 3) / 2
    # We need p <= limit, so i <= (limit - 3) / 2
    for i in range((limit - 3) // 2 + 1):
        if is_prime[i]:
            p = 2 * i + 3  # The actual prime
            # Start at p^2, mark all odd multiples
            start = (p * p - 3) // 2
            is_prime[start::p] = b'\x00' * ((size - start + p - 1) // p)
    
    # Build result: 2 followed by all odd primes
    primes = [2]
    primes.extend(2 * i + 3 for i in range(size) if is_prime[i])
    return primes