"""Optimized Sieve of Eratosthenes for primes_up_to(n)."""


def primes_up_to(n: int) -> list[int]:
    """Return sorted list of all primes <= n.

    Optimized for n up to 2,000,000 using:
    - bytearray for compact memory
    - Skip even numbers (except 2)
    - Slice assignment for fast marking
    """
    if n < 2:
        return []

    # 2 is the only even prime
    if n == 2:
        return [2]

    # Sieve for odd numbers only: index i represents number 3 + 2*i
    # So we need to represent odd numbers from 3 to n
    size = (n - 1) // 2  # count of odd numbers >= 3 and <= n
    sieve = bytearray(size)  # 0 = prime candidate, 1 = composite

    # Only need to check odd primes up to sqrt(n)
    limit = int(n**0.5) + 1

    for i in range(size):
        p = 3 + 2 * i  # the odd number represented by index i
        if p > limit:
            break
        if sieve[i] == 0:  # p is prime
            # Mark all odd multiples of p starting from p^2
            # p^2 is always odd (odd * odd = odd)
            # Find index of p^2: (p^2 - 3) // 2
            start = (p * p - 3) // 2
            # Mark multiples: p^2, p^2+2p, p^2+4p, ...
            # Step in index space is p (since we skip evens)
            sieve[start::p] = b'\x01' * ((size - start + p - 1) // p)

    # Build result: start with 2, then collect remaining primes
    primes = [2]
    primes.extend(3 + 2 * i for i in range(size) if sieve[i] == 0)
    return primes