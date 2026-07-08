def primes_up_to(n):
    if n < 2:
        return []
    size = (n - 3) // 2 + 1
    sieve = bytearray([True]) * size
    for i in range(0, int((n**0.5)-3)//2 + 1):
        if sieve[i]:
            current = 2*i + 3
            start_idx = (current*current -3)//2
            if start_idx < 0:
                start_idx = i+i+1  # Handle when start is less than 0 for small n
            sieve[start_idx::current] = bytearray([False]) * len(sieve[start_idx::current])
    primes = [2]
    for i in range(size):
        if sieve[i]:
            primes.append(2*i +3)
    return primes