def primes_up_to(n: int) -> list[int]:
    """
    Finds all prime numbers less than or equal to n using an optimized Sieve of Eratosthenes.

    Args:
        n: The upper limit (inclusive).

    Returns:
        A sorted list of prime numbers <= n. Returns an empty list if n < 2.
    """
    if n < 2:
        return []
    
    # Handle the special case for prime number 2.
    primes = [2]
    
    if n < 3:
        return primes

    # Step 1: Initialization using bytearray for memory efficiency, focusing on odd numbers.
    # We only need to track odd numbers from 3 up to n.
    # The index i in the array corresponds to the number 2*i + 3.
    
    # Size calculation: Number of odd integers from 3 to n inclusive.
    size = (n - 1) // 2 # This covers indices for 3, 5, ..., up to n or n-1
    is_prime = bytearray(size, 1) # Initialize all as True

    # Sieve process: Iterate through potential primes p
    p = 3
    while p * p <= n:
        # Check if p is marked as prime
        if is_prime[(p - 3) // 2]:
            # Start marking multiples of p.
            # The first multiple to mark is p*p.
            start_multiple = p * p
            
            # We need to find the index corresponding to start_multiple (which must be odd).
            # Since p is odd, p*p is odd. Index = (p*p - 3) // 2
            start_index = (start_multiple - 3) // 2
            
            # Step assignment: Mark all multiples of p as composite.
            # Multiples are p*p, p*(p+2), p*(p+4), ...
            # The difference between consecutive odd multiples is 2*p.
            step = p * 2
            
            for i in range(start_index, size, step):
                is_prime[i] = 0 # Mark as False (composite)
        
        p += 2 # Only check odd numbers

    # Step 3: Collect results (Odd primes)
    for i in range(size):
        if is_prime[i] == 1:
            # Convert index back to the actual number: num = 2*i + 3
            num = 2 * i + 3
            primes.append(num)
            
    return primes

if __name__ == '__main__':
    # Test case 1: Edge case n < 2
    print(f"Primes up to 1: {primes_up_to(1)}") # Expected: []
    print(f"Primes up to 0: {primes_up_to(0)}") # Expected: []

    # Test case 2: Small number
    print(f"Primes up to 10: {primes_up_to(10)}") # Expected: [3, 5, 7]

    # Test case 3: Larger number (testing performance/correctness)
    N = 2000000
    print(f"Calculating primes up to {N}...")
    import time
    start_time = time.time()
    prime_list = primes_up_to(N)
    end_time = time.time()
    
    print(f"Found {len(prime_list)} primes.")
    # print(f"First 10 primes: {prime_list[:10]}") # Optional verification
    print(f"Execution time for N={N}: {end_time - start_time:.4f} seconds")