def primes_up_to(n):
    """
    Returns a sorted list of all prime numbers up to n (inclusive).
    Uses an optimized Sieve of Eratosthenes with bytearray and slice assignment.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]
    if n == 3:
        return [2, 3]

    # The sieve will store odd numbers starting from 3.
    # Index i corresponds to the number (2*i + 3).
    # Max index k satisfies 2*k + 3 <= n  =>  2*k <= n - 3  =>  k <= (n-3)//2.
    size = (n - 3) // 2 + 1
    is_prime = bytearray([1]) * size

    # The first odd prime is 3, which is at index 0.
    # We only need to sieve up to sqrt(n).
    limit = int(n**0.5)
    for p in range(3, limit + 1, 2):
        idx = (p - 3) // 2
        if is_prime[idx]:
            # The first multiple of p to mark is p*p.
            # Its index is (p*p - 3) // 2.
            start = (p * p - 3) // 2
            # The step in our odd-only array is p.
            # Because we only store odds, and p is odd, the distance between 
            # consecutive odd multiples of p (e.g., p*(j), p*(j+2)) 
            # in terms of values is 2p. In our index mapping (divide by 2), 
            # the step is p.
            num_to_mark = (size - 1 - start) // p + 1
            is_prime[start::p] = bytes([0]) * num_to_mark

    primes = [2]
    # Indices where is_prime[i] is still 1 correspond to primes.
    # We skip index 0 if it's not handled correctly, but here we start from 3.
    # Actually, our loop starts from p=3, and the smallest odd prime is 3 at idx 0.
    # If n >= 3, idx 0 (number 3) will be 1 unless it was marked by something smaller.
    # Since we start sieving from p=3, nothing marks index 0.
    for i in range(size):
        if is_prime[i]:
            primes.append(2 * i + 3)
            
    return primes

if __name__ == "__main__":
    # Test cases
    import sys
    
    def test():
        assert primes_up_to(1) == []
        assert primes_up_to(2) == [2]
        assert primes_up_to(3) == [2, 3]
        assert primes_up_to(10) == [2, 3, 5, 7]
        assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
        print("Small tests passed.")

    test()
    
    # Performance test for n = 2,000,000
    import time
    n = 2000000
    start_time = time.time()
    result = primes_up_to(n)
    end_time = time.time()
    print(f"Primes up to {n}: found {len(result)} primes in {end_time - start_time:.4f} seconds.")
    # Expected count for 2M is 148933
    assert len(result) == 148933
