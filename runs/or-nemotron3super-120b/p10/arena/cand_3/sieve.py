def primes_up_to(n):
    """Return a sorted list of primes <= n using an optimized sieve of Eratosthenes.
    Uses bytearray, skips even numbers, and slice assignment for speed.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]
    # Size for odd numbers: index i represents number 2*i+1
    size = (n + 1) // 2
    sieve = bytearray(b'\x00') * size  # 0 means prime candidate
    # Sieve limit for odd numbers up to sqrt(n)
    limit = int(n ** 0.5)
    for i in range(3, limit + 1, 2):
        if sieve[i // 2]:
            continue  # already marked as composite
        start = i * i
        step = 2 * i
        # Number of multiples to mark
        count = ((n - start) // step) + 1
        # Mark multiples: sieve[start//2 :: i] corresponds to numbers start, start+2i, start+4i, ...
        sieve[start // 2 :: i] = b'\x01' * count
    # Collect primes: 2 plus odd numbers where sieve[i] == 0
    primes = [2]
    primes.extend(2 * i + 1 for i in range(1, size) if not sieve[i])
    return primes