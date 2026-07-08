import math

def primes_up_to(n: int) -> list[int]:
    """
    Generates a sorted list of prime numbers less than or equal to n using 
    the Sieve of Eratosthenes, optimized for speed and memory usage.

    Args:
        n: The upper limit (inclusive).

    Returns:
        A sorted list of primes <= n.
    """
    if n < 2:
        return []
    
    # Handle the prime 2 separately
    primes = [2]
    
    if n == 2:
        return primes

    # Optimization: Only store odd numbers >= 3.
    # The index i corresponds to the number 2*i + 1.
    # We need indices up to (n - 1) / 2, which is floor((n-1)/2).
    limit_odd = (n - 1) // 2
    
    # Initialize sieve array: True means potentially prime.
    # Size is limit_odd + 1 because indexing starts at 0 for the number 3.
    is_prime = bytearray([1]) * (limit_odd + 1)

    # The loop runs up to sqrt(n)
    sqrt_n = int(math.sqrt(n))
    
    # Iterate through potential prime numbers p, where p = 2*i + 1
    # i ranges from 0 up to limit_odd (or until the corresponding p exceeds sqrt_n)
    for i in range(limit_odd + 1):
        p = 2 * i + 1
        if p > sqrt_n:
            break
            
        # Check if p is still marked as prime
        if is_prime[i] == 1:
            # p is prime. Mark all its multiples (starting from p*p) as composite.
            # Multiples are of the form k * p. We only care about odd multiples, 
            # since even multiples were handled by skipping evens earlier.
            
            # Smallest odd multiple >= p*p:
            start_k = (p * p + 1) // 2
            
            # The step size in terms of index i corresponds to p/2, but we need 
            # the difference between consecutive odd multiples.
            # Multiples are p*k where k >= p and k is odd if p is odd.
            # If p=3, multiples: 9, 15, 21... (odd multiples) -> steps of 6/2 = 3 in index i
            # General step size for odd numbers is p. Since we are indexing by 
            # half the number, the step size in indices is p // 2 if p is odd.
            step_in_index = p

            # Start marking from p*p (which corresponds to index i_start)
            i_start = (p * p - 1) // 2
            
            # Mark multiples: j = i_start, i_start + step, ...
            for j in range(i_start, limit_odd + 1, step_in_index):
                is_prime[j] = 0

    # Collect the results
    for i in range(limit_odd + 1):
        if is_prime[i] == 1:
            p = 2 * i + 1
            primes.append(p)
            
    return primes

if __name__ == '__main__':
    # Test cases
    print("Primes up to 10:", primes_up_to(10)) # Expected: [2, 3, 5, 7]
    print("Primes up to 2:", primes_up_to(2))   # Expected: [2]
    print("Primes up to 1:", primes_up_to(1))   # Expected: []
    
    N_large = 20 # Test a slightly larger number for verification
    result = primes_up_to(N_large)
    print(f"Primes up to {N_large}: {result}")

    # Testing the performance target (n=2,000,000) is done by running the code, 
    # but we ensure the structure supports it.
    N_target = 2_000_000
    print(f"Testing large N={N_target}. Generating primes...")
    import time
    start_time = time.time()
    large_primes = primes_up_to(N_target)
    end_time = time.time()
    
    count = len(large_primes)
    print(f"Found {count} primes up to {N_target}. Time taken: {end_time - start_time:.4f} seconds.")

