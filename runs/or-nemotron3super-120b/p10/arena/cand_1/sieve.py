def primes_up_to(n):
    """Return a sorted list of all prime numbers <= n.

    Uses an optimized Sieve of Eratosthenes:
    - Handles n < 2 returning empty list.
    - Treats 2 separately, then sieves only odd numbers.
    - Uses a bytearray for memory efficiency.
    - Uses slice assignment for fast marking of composites.
    """
    if n < 2:
        return []
    # 2 is prime
    primes = [2]
    if n < 3:
        return primes

    # Number of odd candidates from 3 to n inclusive.
    sieve_len = (n - 1) // 2
    sieve = bytearray(b'\x01') * sieve_len  # 1 means assumed prime

    limit = int(n**0.5)
    for i in range(sieve_len):
        if sieve[i]:
            p = 2 * i + 3          # the actual prime number
            if p > limit:
                break
            # Start marking at p*p (which is odd). Convert to index.
            start = (p * p - 3) // 2
            # Step in index space is p (since we skip even multiples).
            if start < sieve_len:
                sieve[start::p] = b'\x00' * ((sieve_len - start - 1) // p + 1)

    # Collect remaining primes from the sieve.
    primes.extend(2 * i + 3 for i, v in enumerate(sieve) if v)
    return primes