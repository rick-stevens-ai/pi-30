def primes_up_to(n: int) -> list[int]:
    """
    Finds all prime numbers less than or equal to n using the Sieve of Eratosthenes.

    Args:
        n: The upper limit (inclusive).

    Returns:
        A sorted list of prime numbers <= n. Returns an empty list if n < 2.
    """
    if n < 2:
        return []

    # Initialize sieve: Use a boolean array (bytearray is efficient)
    # Size n+1, initialized to True (potential primes)
    is_prime = bytearray([True] * (n + 1))
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= n:
        # If is_prime[p] is not changed, then it is a prime
        if is_prime[p]:
            # Mark all multiples of p starting from p*p as not prime
            # This optimization starts at p*p because smaller multiples (like 2p, 3p)
            # would have already been marked by smaller primes.
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1

    # Collect all prime numbers
    primes = []
    for p in range(2, n + 1):
        if is_prime[p]:
            primes.append(p)

    return primes

if __name__ == '__main__':
    # Test case for edge case n < 2
    print(f"Primes up to 1: {primes_up_to(1)}") # Expected: []
    print(f"Primes up to 2: {primes_up_to(2)}") # Expected: [2]
    print(f"Primes up to 10: {primes_up_to(10)}") # Expected: [2, 3, 5, 7]
    
    # Test case for larger number (e.g., n=2,000,000)
    N = 2000000
    import time
    start_time = time.time()
    prime_list = primes_up_to(N)
    end_time = time.time()
    
    print(f"Found {len(prime_list)} primes up to {N}.")
    # print(f"First 10 primes: {prime_list[:10]}") # Uncomment to see first few
    print(f"Execution time for N={N}: {end_time - start_time:.4f} seconds")