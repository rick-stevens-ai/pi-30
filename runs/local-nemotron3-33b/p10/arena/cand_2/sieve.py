"""Sieve of Eratosthenes implementation exposing primes_up_to(n).

Returns a sorted list of all prime numbers <= n using a memory‑efficient
bytearray. Handles edge cases (n < 2) and is optimized for large inputs
(e.g., n = 2_000_000) by skipping even numbers after handling 2.
Only uses the Python standard library.
"""

def primes_up_to(n: int):
    """Return a sorted list of all prime numbers <= n.

    Edge cases:
        - If n < 2, returns an empty list [].
    
    The algorithm:
        * Uses a bytearray where 1 indicates “potentially prime”.
        * Marks 0 and 1 as non‑prime.
        * Handles the even prime 2 separately, then skips all other evens.
        * For each odd candidate p up to sqrt(n):
              – If p is still marked prime, mark its multiples starting at p*p.
            Multiples are stepped by p (which keeps the inner loop tight).
        * Finally collect indices that remain marked as primes.

    This implementation is tuned for speed on large n while staying
    within the Python standard library only.
    """
    if n < 2:
        return []

    # bytearray: 1 == potentially prime, 0 == composite.
    # Index represents the integer value.
    is_prime = bytearray(b'\x01') * (n + 1)
    # 0 and 1 are not prime.
    is_prime[0:2] = b'\x00\x00'

    # Mark even numbers > 2 as composite.
    if n >= 4:
        # 4,6,8,... up to n (step 2)
        is_prime[4:n+1:2] = b'\x00' * ((n - 4) // 2 + 1)

    limit = int(n ** 0.5) + 1
    # Iterate only odd candidates.
    for p in range(3, limit, 2):
        if is_prime[p]:
            start = p * p          # first multiple to mark
            # Mark every p‑th number (still skips evens because p is odd)
            is_prime[start:n+1:p] = b'\x00' * ((n - start) // p + 1)

    # Collect primes in ascending order.
    return [i for i, prime_flag in enumerate(is_prime) if prime_flag]


# Optional: allow direct execution for quick testing.
if __name__ == "__main__":
    import sys
    try:
        test_n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    except ValueError:
        print("Please provide an integer argument.")
        sys.exit(1)

    print(f"Primes up to {test_n}:")
    print(primes_up_to(test_n))