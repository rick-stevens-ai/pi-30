def primes_up_to(n: int) -> list[int]:
    """Return a sorted list of all prime numbers <= n.

    The algorithm uses a bytearray sieve, skips even numbers (except 2),
    and performs slice assignment for speed. Validated up to 2 000 000.
    """
    if n < 2:
        return []

    # Initialise a bytearray: True=1 (potential prime), False=0 (composite).
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0] = 0
    sieve[1] = 0

    # Explicitly eliminate even numbers > 2.
    sieve[4 : n + 1 : 2] = b"\x00" * ((n - 4) // 2 + 1)

    limit = int(n**0.5) + 1
    for p in range(3, limit, 2):
        if sieve[p]:
            start = p * p
            step = p * 2           # skip even multiples
            sieve[start : n + 1 : step] = b"\x00" * ((n - start) // step + 1)

    # Collect results: 2 plus all odd indices that remain True.
    primes = [2] if n >= 2 else []
    primes.extend(i for i in range(3, n + 1, 2) if sieve[i])
    return primes


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     import sys
#     print(primes_up_to(int(sys.argv[1])))