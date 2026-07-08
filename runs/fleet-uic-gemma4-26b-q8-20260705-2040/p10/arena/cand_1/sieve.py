def primes_up_to(n: int) -> list[int]:
    """
    Returns a sorted list of all prime numbers up to and including n.
    Optimized using bytearray, skipping even numbers, and slice assignment.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]

    # size represents the number of odd integers from 1 up to n.
    # The number at index i is (2*i + 1).
    size = (n - 1) // 2 + 1
    sieve = bytearray([1]) * size
    sieve[0] = 0  # 1 is not prime

    # We only need to sieve up to sqrt(n).
    limit = int(n**0.5)
    for i in range(1, (limit // 2) + 1):
        if sieve[i]:
            p = 2 * i + 1
            # Smallest multiple of p to mark is p*p.
            # Its index is (p*p - 1) // 2.
            start = (p * p - 1) // 2
            if start < size:
                # Mark multiples: p*p, p*(p+2), p*(p+4)... in terms of indices.
                # The index increment is (p*(m+2)-1)//2 - (p*m-1)//2 = p.
                num_multiples = (size - 1 - start) // p + 1
                sieve[start::p] = bytearray(num_multiples)

    return [2] + [2 * i + 1 for i in range(1, size) if sieve[i]]


if __name__ == "__main__":
    import time
    
    # Test correctness
    assert primes_up_to(1) == []
    assert primes_up_to(2) == [2]
    assert primes_up_to(10) == [2, 3, 5, 7]
    assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    print("Correctness tests passed!")

    # Benchmark
    n = 2_000_000
    start_time = time.perf_counter()
    primes = primes_up_to(n)
    end_time = time.perf_counter()
    print(f"Found {len(primes)} primes up to {n:,} in {end_time - start_time:.4f} seconds.")
