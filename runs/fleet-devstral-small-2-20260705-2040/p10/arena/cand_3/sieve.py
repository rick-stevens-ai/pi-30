def primes_up_to(n):
    """Return a sorted list of primes <= n.
    
    Uses the Sieve of Eratosthenes with optimizations:
    - Skips even numbers (except 2)
    - Uses bytearray for memory efficiency
    - Uses slice assignment for marking multiples
    
    Time complexity: O(n log log n)
    Space complexity: O(n)
    """
    if n < 2:
        return []
    
    # Special case: n == 2
    if n == 2:
        return [2]
    
    # Initialize sieve for odd numbers only
    # sieve[i] represents the number 2i + 3
    size = (n - 1) // 2
    sieve = bytearray([1]) * size
    
    # 3 is the first odd prime
    for i in range(0, int((n ** 0.5 - 1) / 2) + 1):
        if sieve[i]:
            # The current prime is 2i + 3
            # Mark multiples starting from (current_prime)^2
            current_prime = 2 * i + 3
            start = (current_prime * current_prime - 3) // 2
            # Step size is current_prime (since we only store odd numbers)
            step = current_prime
            # Mark all multiples
            sieve[start::step] = b'\x00' * len(sieve[start::step])
    
    # Collect primes
    primes = [2] if n >= 2 else []
    primes.extend(2 * i + 3 for i in range(size) if sieve[i])
    
    return primes


if __name__ == "__main__":
    # Test cases
    assert primes_up_to(1) == []
    assert primes_up_to(2) == [2]
    assert primes_up_to(10) == [2, 3, 5, 7]
    assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    
    # Performance test
    import time
    n = 2_000_000
    start = time.time()
    primes = primes_up_to(n)
    end = time.time()
    
    print(f"Found {len(primes)} primes up to {n} in {end - start:.4f} seconds")
    print(f"First 10 primes: {primes[:10]}")
    print(f"Last 10 primes: {primes[-10:]}")
