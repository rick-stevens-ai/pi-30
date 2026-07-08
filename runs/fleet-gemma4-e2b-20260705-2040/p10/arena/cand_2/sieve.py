def primes_up_to(n: int) -> list[int]:
    """
    Finds all prime numbers up to n using the Sieve of Eratosthenes.

    Args:
        n: The upper limit (inclusive).

    Returns:
        A sorted list of prime numbers less than or equal to n.
    """
    if n < 2:
        return []

    # Initialize a boolean array for all numbers up to n.
    # is_prime[i] will be False if i is composite. Size n+1 for indices 0 to n.
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime

    p = 2
    while p * p <= n:
        if is_prime[p]:
            # Mark all multiples of p starting from p*p as not prime.
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1

    primes = []
    # Collect all numbers i where is_prime[i] is True
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)

    return primes