def primes_up_to(n: int) -> list[int]:
    """
    Return a sorted list of all prime numbers <= n.

    The implementation uses a bytearray-based Sieve of Eratosthenes:
      * Handles n < 2 by returning an empty list.
      * Treats 2 as a special case and then processes only odd numbers.
      * Skips even multiples by stepping with ``p*2``.
      * Uses slice assignment for fast bulk marking of composites.
    The algorithm runs in O(n log log n) time and uses only the Python
    standard library.
    """
    # 1. Guard against invalid/edge inputs
    if n < 2:
        return []

    # 2. Fast path for very small n to avoid unnecessary work
    if n == 2:
        return [2]

    # 3. Create a bytearray where index i indicates whether i is still considered prime.
    #    We allocate space up to n inclusive.
    sieve = bytearray(b'\x01') * (n + 1)
    # 4. Explicitly mark 0,1 and all even numbers >2 as non‑prime
    sieve[0:2] = b'\x00\x00'                     # 0 and 1 are not prime
    sieve[4::2] = b'\x00' * ((n - 4) // 2 + 1)   # even numbers >=4

    limit = int(n ** 0.5) + 1                    # only need to iterate up to sqrt(n)
    # 5. Process odd candidates starting at 3
    for p in range(3, limit, 2):
        if sieve[p]:
            # start striking out at p*p (the first composite that hasn't been crossed out yet)
            start = p * p
            step = p << 1                        # equivalent to p*2, skips even multiples
            count = (n - start) // step + 1      # number of elements in slice sieve[start::step]
            sieve[start:start + step * count:step] = b'\x00' * count

    # 6. Collect the primes: 2 plus all odd indices that remain marked as prime
    result = [2]
    # Append each odd i where sieve[i]==1 (prime)
    for i in range(3, n + 1, 2):
        if sieve[i]:
            result.append(i)

    return result