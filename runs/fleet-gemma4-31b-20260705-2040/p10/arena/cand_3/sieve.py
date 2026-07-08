def primes_up_to(n):
    """
    Returns a sorted list of primes up to n using an optimized Sieve of Eratosthenes.
    
    Optimizations used:
    - bytearray for memory efficiency and speed.
    - Skipping even numbers in the sieve array.
    - Slice assignment for fast marking of non-primes.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]

    # We only store odd numbers starting from 3.
    # Index i represents the number (2*i + 1).
    # The largest index needed is for the largest odd number <= n.
    # If n is even, max odd is n-1. If n is odd, max odd is n.
    # size = ((n - 1) // 2) + 1  -- but we need to be careful with indexing.
    
    # Let's use a simpler mapping: sieve[i] corresponds to number i.
    # To save space and time, we can still skip evens by using a bytearray 
    # of size (n // 2) + 1 where index i maps to 2*i + 1.
    
    size = (n - 1) // 2 + 1
    sieve = bytearray([1]) * size
    sieve[0] = 0  # 1 is not prime

    # Sieve odd numbers starting from 3
    # 3 is index 1, 5 is index 2, etc.
    limit = int(n**0.5)
    for i in range(1, (limit // 2) + 1):
        if sieve[i]:
            p = 2 * i + 1
            # Start marking from p*p.
            # The index of p*p is (p*p - 1) // 2.
            start = (p * p - 1) // 2
            if start >= size:
                break
            # Mark every p-th odd number as non-prime.
            # The distance between (2i+1) and (2(i+p)+1) is p indices.
            sieve[start::p] = b'\x00' * ((size - 1 - start) // p + 1)

    primes = [2]
    primes.extend([2 * i + 1 for i in range(1, size) if sieve[i]])
    return primes

if __name__ == "__main__":
    import time
    n = 2_000_000
    start = time.time()
    res = primes_up_to(n)
    end = time.time()
    print(f"Found {len(res)} primes up to {n} in {end - start:.4f}s")
    # Validation
    assert res[0] == 2
    assert res[-1] <= n
    if n >= 3:
        assert res[1] == 3
