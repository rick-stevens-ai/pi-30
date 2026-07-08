def count_primes(n):
    if n <= 2:
        return 0

    # Initialize sieve array (bytearray for memory efficiency)
    is_prime = bytearray(n)
    for i in range(n):
        is_prime[i] = 1  # Assume all are prime initially

    is_prime[0] = is_prime[1] = 0

    # Handle multiples of 2
    for i in range(4, n, 2):
        is_prime[i] = 0

    # Sieve process for odd primes
    limit = int(n**0.5) + 1
    for p in range(3, limit, 2):
        if is_prime[p] == 1:
            start = p * p
            # Mark all ODD multiples of p starting from p*p
            i = start
            while i < n:
                is_prime[i] = 0
                i += 2 * p

    # Count the primes
    return sum(is_prime)
