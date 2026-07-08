def primes_up_to(n):
    """Returns a sorted list of primes up to n."""
    if n < 2:
        return []
    if n == 2:
        return [2]

    # Represents odd numbers starting from 1. Index i corresponds to 2i + 1.
    num_odds = (n - 1) // 2 + 1
    is_prime = bytearray([1]) * num_odds
    is_prime[0] = 0  # 1 is not prime

    for p in range(3, int(n**0.5) + 1, 2):
        if is_prime[p // 2]:
            start = (p * p) // 2
            # The number of elements to replace
            count = (num_odds - 1 - start) // p + 1
            is_prime[start::p] = bytes(count)

    return [2] + [2 * i + 1 for i in range(1, num_odds) if is_prime[i]]

if __name__ == "__main__":
    import time
    
    # Test correctness
    test_n = 30
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert primes_up_to(test_n) == expected
    assert primes_up_to(1) == []
    assert primes_up_to(2) == [2]
    print("Correctness tests passed.")

    # Performance test
    n = 2_000_000
    start_time = time.time()
    primes = primes_up_to(n)
    end_time = time.time()
    print(f"Found {len(primes)} primes up to {n} in {end_time - start_time:.4f} seconds")
