"""Sieve of Eratosthenes — bytearray + skip-evens + slice-assign."""


def primes_up_to(n: int) -> list[int]:
    """Return sorted list of all primes <= n.

    Uses a bytearray indexed over the odd numbers (2*i+1).  Even positions
    are implicit, so marking every *i*-th index from ``p*p//2`` strikes out
    the odd multiples of p starting at p².  Slice assignment is used for
    bulk zeroing of composites.

    Reference: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes#Optimisation_notes
    """
    if n < 2:
        return []

    # For tiny ranges, avoid the overhead of the full sieve machinery.
    if n == 2:
        return [2]
    if n == 3:
        return [2, 3]

    limit = (n + 1) // 2     # number of odd slots (index i → value 2*i+1); covers all odds ≤ n
    sieve = bytearray(limit)  # all zeros → assumed prime

    for p in range(3, int(n ** 0.5) + 1, 2):
        start = (p * p) // 2
        sieve[start::p] = b'\x01' * len(sieve[start::p])

    # Collect: always include 2, then odd values still zero in the sieve.
    # Collect: always include 2, then odd values still zero in the sieve.
    # Start at i=1 because index 0 represents value 1 (not prime).
    # Index 0 represents value 1 (not prime), so skip it.
    result = [2]
    for i in range(1, limit):
        if not sieve[i]:
            result.append(2 * i + 1)

    return result


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import time

    n = 2_000_000
    t0 = time.perf_counter()
    primes = primes_up_to(n)
    dt = time.perf_counter() - t0
    print(f"primes_up_to({n}) → {len(primes)} primes in {dt:.4f}s")
