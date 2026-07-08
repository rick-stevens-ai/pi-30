def primes_up_to(n):
    """Returns a sorted list of primes up to n."""
    if n < 2:
        return []
    if n == 2:
        return [2]

    # Sieve odd numbers only. Index i represents 2*i + 1.
    # The largest odd number <= n is (n if n % 2 != 0 else n - 1).
    # Let that be 2k + 1. Then k = (max_odd - 1) // 2.
    # Size required: k + 1 elements to include index k.
    size = (n + 1) // 2
    sieve = bytearray([1]) * size
    
    # Index 0 is number 1, which is not prime.
    sieve[0] = 0
    
    limit = int(n**0.5)
    for p in range(3, limit + 1, 2):
        if sieve[p // 2]:
            # Start at p*p. The index for p*p is (p*p - 1) // 2.
            start = (p * p - 1) // 2
            # Step in numbers is 2p, so step in indices is p.
            # Corrected: p-th odd number after i? No.
            # If current index is i (representing 2i+1), the next multiple of p is 2(i+p)+1 = (2i+1) + 2p.
            # So step in indices is indeed p.
            num_elements = len(range(start, size, p))
            if num_elements > 0:
                sieve[start::p] = b'\x00' * num_elements

    # Construct the list of primes.
    primes = [2]
    for i in range(1, size):
        if sieve[i]:
            primes.append(2 * i + 1)
            
    return primes

if __name__ == "__main__":
    import time
    
    # Test small n
    print(f"n=1: {primes_up_to(1)}")
    print(f"n=2: {primes_up_to(2)}")
    print(f"n=10: {primes_up_to(10)}")
    print(f"n=30: {primes_up_to(30)}")

    # Test performance
    N = 2_000_000
    start_time = time.time()
    res = primes_up_to(N)
    end_time = time.time()
    print(f"n={N}: found {len(res)} primes in {end_time - start_time:.4f}s")
    
    # Quick verification of some expected results
    # Primes up to 10: 2, 3, 5, 7 (count 4)
    assert primes_up_to(10) == [2, 3, 5, 7]
    # n=1 should be []
    assert primes_up_to(1) == []
    # n=2 should be [2]
    assert primes_up_to(2) == [2]
