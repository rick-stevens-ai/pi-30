# P23 SEED: trial division for every number. Correct but slow.
def count_primes(n):
    if n < 3:
        return 0
    if n == 3:
        return 1
    
    # Only sieve odd numbers: index i represents number 2*i+1
    # Index 0 represents 1 (not prime), index 1 represents 3, etc.
    size = (n + 1) // 2
    sieve = bytearray(b'\x01') * size
    sieve[0] = 0  # 1 is not prime
    
    limit = int(n ** 0.5) + 1
    for i in range(3, limit, 2):
        if sieve[i // 2]:
            # Start marking from i*i, step by 2*i (only odd multiples)
            start = i * i
            step = i * 2
            sieve[start // 2 :: i] = b'\x00' * ((size - start // 2 - 1) // i + 1)
    
    # +1 for the prime number 2
    return sum(sieve) + 1
