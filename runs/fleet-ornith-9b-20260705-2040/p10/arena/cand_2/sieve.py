def primes_up_to(n):
    """Return sorted list of all primes <= n using a compacted Sieve of Eratosthenes.

    Only odd composites are tracked in the bytearray, and slice-assignment marks
    each prime's multiples.  Stdlib only.
    """
    if n < 2:
        return []

    # Compact sieve: index i represents odd number (2*i + 1).
    # Size = count of odd numbers in [1, n]; index i represents 2*i+1.
    size = (n - 1) // 2 + 1

    # All bits set → assume prime until proven otherwise.
    is_prime = bytearray(b'\x01') * size

    limit = int(n ** 0.5)
    for i in range(3, limit + 1, 2):
        start = (i * i - 1) >> 1          # index of i² in the compacted sieve
        if start >= size:
            break
        num = (size - 1 - start) // i + 1
        is_prime[start::i] = b'\x00' * num

    out = [2] if n >= 2 else []
    for i in range(1, size):               # skip index 0 (represents "1")
        if is_prime[i]:
            out.append(i << 1 | 1)         # reverse: number = 2*i + 1

    return out
