def primes_up_to(n):
    if n < 2:
        return []
    if n == 2:
        return [2]
    
    # size represents number of odd integers from 1 to n
    # indices represent (val - 1) // 2
    # val = 2 * idx + 1
    size = (n - 1) // 2 + 1
    is_prime = bytearray([1]) * size
    is_prime[0] = 0  # index 0 -> value 1, not prime
    
    limit = int(n**0.5)
    for p_idx in range(1, (limit // 2) + 1):
        if is_prime[p_idx]:
            p = 2 * p_idx + 1
            start = (p * p - 1) // 2
            is_prime[start::p] = bytearray(len(range(start, size, p)))

    return [2] + [2 * i + 1 for i in range(1, size) if is_prime[i]]

if __name__ == "__main__":
    import time
    n = 2000000
    start_time = time.time()
    primes = primes_up_to(n)
    end_time = time.time()
    print(f"Found {len(primes)} primes up to {n} in {end_time - start_time:.4f}s")
    print(f"Last 5 primes: {primes[-5:]}")
