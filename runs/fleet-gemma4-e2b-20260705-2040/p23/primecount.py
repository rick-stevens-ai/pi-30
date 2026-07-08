def count_primes(n):
    if n <= 2:
        return 0
    is_prime = bytearray(n)
    for i in range(2, n):
        is_prime[i] = 1

    # Sieve of Eratosthenes: Mark multiples of primes as not prime
    p = 2
    while p * p < n:
        if is_prime[p] == 1:
            # Mark all multiples of p starting from p*p as not prime
            for i in range(p * p, n, p):
                is_prime[i] = 0
        p += 1

    # Count primes
    count = sum(1 for i in range(2, n) if is_prime[i] == 1)
    return count
