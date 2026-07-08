def primes_up_to(n):
    """Return sorted list of all primes ≤ n using an odd-only sieve."""
    if n < 2:
        return []
    if n == 2:
        return [2]

    # Track only odd candidates ≥ 3: index i ↔ number (2i + 3)
    limit = (n - 1) // 2
    sieve = bytearray(b'\x01') * limit

    sqrt_limit = int(limit**0.5)
    for i in range(sqrt_limit + 1):
        if i >= limit:
            break
        p = 2 * i + 3
        if not sieve[i]:
            continue
        # First odd composite of p is p²; step by 2p in original space → step p here
        start = (p * p - 3) // 2
        sieve[start::p] = b'\x00' * len(sieve[start::p])

    return [2] + [2 * i + 3 for i, v in enumerate(sieve) if v]
