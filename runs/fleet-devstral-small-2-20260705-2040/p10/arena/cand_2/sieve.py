def primes_up_to(n):
    """Return a sorted list of primes <= n.
    
    Uses the Sieve of Eratosthenes algorithm with optimizations:
    - Skips even numbers (except 2)
    - Uses bytearray for memory efficiency
    - Uses slice assignment for marking multiples
    
    Time complexity: O(n log log n)
    Space complexity: O(n)
    """
    if n < 2:
        return []
    if n == 2:
        return [2]
    
    # Initialize sieve for odd numbers only
    # sieve[i] = 0 means i*2+1 is prime
    # sieve[i] = 1 means i*2+1 is composite
    size = (n + 1) // 2
    sieve = bytearray([0]) * size
    
    # Mark multiples of 3 starting from 3*3=9
    # Step through multiples: 3*3, 3*5, 3*7, ...
    for i in range(1, size):
        if sieve[i] == 0:
            prime = 2 * i + 1
            # Mark multiples starting from prime^2
            start = prime * prime
            # Convert to index: (start-1)//2
            # Step by 2*prime (since we skip evens)
            idx = (start - 1) // 2
            if idx < size:
                sieve[idx::prime] = b'\x01' * len(sieve[idx::prime])
    
    # Collect primes
    primes = [2]  # 2 is the only even prime
    primes.extend(2 * i + 1 for i in range(1, size) if sieve[i] == 0)
    
    return primes


if __name__ == "__main__":
    # Test cases
    assert primes_up_to(1) == []
    assert primes_up_to(2) == [2]
    assert primes_up_to(10) == [2, 3, 5, 7]
    assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    
    # Performance test
    import time
    start = time.time()
    primes = primes_up_to(2_000_000)
    end = time.time()
    print(f"Found {len(primes)} primes up to 2,000,000 in {end - start:.4f} seconds")
    print(f"First 10 primes: {primes[:10]}")
    print(f"Last 10 primes: {primes[-10:]}")
