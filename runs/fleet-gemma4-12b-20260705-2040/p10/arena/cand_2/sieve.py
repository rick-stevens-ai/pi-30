def primes_up_to(n):
    """
    Returns a sorted list of all prime numbers up to and including n.
    Uses an optimized Sieve of Eratosthenes with bytearray, skipping evens,
    and slice assignment for performance.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]
    
    # is_prime[i] represents the number (2*i + 1)
    # Size needed: the largest odd number <= n is either n or n-1.
    # If n=3, max odd is 3, index is 3//2 = 1. size = 2 (indices 0, 1)
    # If n=4, max odd is 3, index is 3//2 = 1. size = 2 (indices 0, 1)
    # Wait, if we use n // 2 + 1 as size:
    # For n=3, size = 3 // 2 + 1 = 2. Indices 0, 1. Numbers 1, 3. Correct.
    # For n=4, size = 4 // 2 + 1 = 3. Indices 0, 1, 2. Numbers 1, 3, 5.
    # We should only consider numbers <= n.
    
    limit = n // 2 + 1
    is_prime = bytearray([1]) * limit
    is_prime[0] = 0  # Number 1 is not prime
    
    for p in range(3, int(n**0.5) + 1, 2):
        if is_prime[p // 2]:
            # The multiples of p are p*p, p*(p+2), p*(p+4)...
            # These correspond to indices: (p*p)//2, (p*(p+2))//2, ...
            # Since p is odd, these are all integers.
            # The step between indices is ((p*(k+2)) - (p*k)) // 2 = p.
            start = (p * p) // 2
            if start < limit:
                is_prime[start :: p] = bytearray([0]) * ((limit - 1 - start) // p + 1)
    
    primes = [2]
    # We only want numbers <= n. 
    # The index i corresponds to 2*i + 1.
    # So we need 2*i + 1 <= n  => 2*i <= n - 1 => i <= (n-1) // 2.
    max_idx = (n - 1) // 2
    for i in range(1, max_idx + 1):
        if is_prime[i]:
            primes.append(2 * i + 1)
            
    return primes

if __name__ == "__main__":
    import sys
    import time

    # Test cases
    print(f"n=10: {primes_up_to(10)}")  # [2, 3, 5, 7]
    print(f"n=2: {primes_up_to(2)}")    # [2]
    print(f"n=1: {primes_up_to(1)}")    # []
    
    # Performance test
    n = 2000000
    start_time = time.time()
    result = primes_up_to(n)
    end_time = time.time()
    print(f"n={n} found {len(result)} primes in {end_time - start_time:.4f}s")
