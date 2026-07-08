def primes_up_to(n):
    """
    Returns a sorted list of all prime numbers less than or equal to n.
    Uses an efficient Sieve of Eratosthenes with bytearray and slice assignment,
    skipping even numbers.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]

    # We only store odd numbers in the sieve to save space and time.
    # Index i corresponds to the number 2*i + 1.
    # The number of elements needed is (n // 2) + 1 if we want to include up to n.
    # Example: n=10, odds are 1, 3, 5, 7, 9. Indices 0, 1, 2, 3, 4. len=5. (10//2)+1 = 6? No.
    # Let's be careful.
    # n=10: 2*i+1 <= 10 => 2*i <= 9 => i <= 4.5 => i can be 0,1,2,3,4. size 5. 
    # (n+1)//2 for odd-only array including 1... let's check.
    # n=1: (1+1)//2 = 1  (index 0 -> 1)
    # n=2: (2+1)//2 = 1  (index 0 -> 1) - but we handle n < 3 separately.
    # n=3: (3+1)//2 = 2  (indices 0, 1 -> values 1, 3)
    # n=4: (4+1)//2 = 2  (indices 0, 1 -> values 1, 3)
    # n=5: (5+1)//2 = 3  (indices 0, 1, 2 -> values 1, 3, 5)
    
    size = (n + 1) // 2
    is_prime = bytearray([1]) * size
    
    # Number 1 is not prime. index 0 corresponds to 2*0+1 = 1.
    is_prime[0] = 0

    limit = int(n**0.5)
    for p in range(3, limit + 1, 2):
        if is_prime[p // 2]:
            # Start sieving from p*p. 
            # Index of p*p is (p*p - 1) // 2.
            start = (p * p) // 2
            # The step in index for odd multiples: 
            # index(v + 2p) = (v + 2p - 1)/2 = index(v) + p.
            step = p
            # Slice assignment: is_prime[start::step] must be assigned a bytes object of the same length.
            # The number of elements to replace is len(range(start, size, step)).
            num_elements = (size - 1 - start) // step + 1
            is_prime[start::step] = b'\x00' * num_elements

    return [2] + [2 * i + 1 for i in range(1, size) if is_prime[i]]

def reference_primes_up_to(n):
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
    return [p for p, prime in enumerate(is_prime) if prime]

def test():
    import sys
    test_cases = [
        (-1,), (0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,),
        (11,), (12,), (13,), (14,), (15,), (25,), (100,), (101,), (997,), (1000,)
    ]
    
    for case in test_cases:
        n = case[0]
        expected = reference_primes_up_to(n)
        actual = primes_up_to(n)
        if expected != actual:
            print(f"FAILED for n={n}: Expected {expected}, got {actual}")
            sys.exit(1)
    
    # Stress test
    import time
    n = 2000000
    print(f"Testing n={n}...")
    start_time = time.time()
    primes = primes_up_to(n)
    end_time = time.time()
    expected_len = len(reference_primes_up_to(n))
    if len(primes) != expected_len:
        print(f"FAILED for n={n}: Expected length {expected_len}, got {len(primes)}")
        sys.exit(1)
    print(f"PASSED! Found {len(primes)} primes in {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    test()
