import math
from typing import List

def primes_up_to(n: int) -> List[int]:
    """
    Generates a sorted list of prime numbers less than or equal to n using 
    an optimized Sieve of Eratosthenes implementation tailored for speed.

    Args:
        n: The upper limit (inclusive).

    Returns:
        A list of primes <= n.
    """
    if n < 2:
        return []

    # Handle 2 separately, as it is the only even prime
    primes = [2]
    if n == 2:
        return primes

    # Optimization: Only sieve odd numbers >= 3.
    # M is the count of odd integers up to n that are greater than or equal to 3.
    # Index i corresponds to the number p = 2i + 3.
    M = (n - 3) // 2 + 1

    # Use bytearray for memory efficiency and fast assignment/lookups.
    is_prime = bytearray([1] * M)

    limit = int(math.sqrt(n))
    
    # We iterate over odd primes p up to sqrt(n).
    # p corresponds to index i: p = 2i + 3.
    # Max index i_max such that 2*i_max + 3 <= limit.
    i_max = (limit - 3) // 2

    for i in range(i_max + 1):
        if is_prime[i] == 1:
            p = 2 * i + 3  # p is the current prime candidate
            
            # Start sieving from p^2. Since we only store odds, we start at p*p.
            # The starting index j corresponds to p*p: j = (p*p - 3) // 2
            start_j = (p * p - 3) // 2
            
            # Step size for indices: multiples of p are spaced by 2p in the full number line.
            # In our odd-only array, the spacing is p.
            step = p

            # Use slice assignment for fast marking of composites.
            for j in range(start_j, M):
                is_prime[j] = 0

    # Collect the results
    for i in range(M):
        if is_prime[i] == 1:
            p = 2 * i + 3
            primes.append(p)
            
    return primes

# Example usage and testing (optional, but good practice)
if __name__ == '__main__':
    # Test edge cases
    print(f"Primes up to 0: {primes_up_to(0)}") # Expected: []
    print(f"Primes up to 1: {primes_up_to(1)}") # Expected: []
    print(f"Primes up to 2: {primes_up_to(2)}") # Expected: [2]

    # Test small case
    print(f"Primes up to 10: {primes_up_to(10)}") # Expected: [2, 3, 5, 7]

    # Test medium case
    N_medium = 100
    print(f"Primes up to {N_medium}: {len(primes_up_to(N_medium))}") # Expected count: 25

    # Test large case (2,000,000) for performance check
    N_large = 2000000
    print(f"Starting sieve up to {N_large}...")
    import time
    start_time = time.time()
    primes_list = primes_up_to(N_large)
    end_time = time.time()
    
    print(f"Finished sieve up to {N_large}. Found {len(primes_list)} primes.")
    print(f"Time taken: {end_time - start_time:.4f} seconds.")
    # Sanity check the last few primes
    if len(primes_list) > 0:
        print(f"Last prime found: {primes_list[-1]}") # Should be <= 2,000,000

