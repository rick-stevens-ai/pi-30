def primes_up_to(n):
    """
    Returns a sorted list of primes up to n.
    Uses an efficient Sieve of Eratosthenes with bytearray and slice assignment.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]
    
    # sieve[i] represents the number (2*i + 1)
    # The size is enough to cover up to n
    limit = n // 2 + 1
    sieve = bytearray([1]) * limit
    sieve[0] = 0  # 1 is not prime

    for i in range(1, int(n**0.5) // 2 + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p - 1) // 2
            # Use slice assignment for high performance
            # The step is p because we only store odd numbers.
            # Multiples of p are p*3, p*5, p*7... which correspond to indices:
            # (3p-1)//2, (5p-1)//2, (7p-1)//2... 
            # The difference between consecutive indices is (2p)/2 = p.
            sieve[start::p] = bytes([0]) * ((limit - 1 - start) // p + 1)

    primes = [2]
    # Only iterate through odd numbers starting from index 1 (which is 3)
    for i in range(1, limit):
        if sieve[i]:
            primes.append(2 * i + 1)
            
    # Filter primes > n because the slice assignment might have gone slightly over
    # Actually, with limit = n // 2 + 1, (2*i+1) <= n is guaranteed if i < limit
    # Let's check: 2*(limit-1)+1 = 2*(n//2)+1. 
    # If n=10, limit=6. i=5 => 2*5+1=11 > 10.
    # So we need to ensure 2*i + 1 <= n
    return [p for p in primes if p <= n]

if __name__ == "__main__":
    import time
    n = 2000000
    start = time.time()
    primes = primes_up_to(n)
    end = time.time()
    print(f"Number of primes up to {n}: {len(primes)}")
    print(f"Time taken: {end - start:.4f} seconds")
