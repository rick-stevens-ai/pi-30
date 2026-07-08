def primes_up_to(n):
    # Handle edge cases
    if n < 2:
        return []
    sieve_size = max(3, (n // 2) + 1)
    sieve = bytearray([True]) * sieve_size
    sieve[0] = False  # 2*0 = 0 not prime
    if n >= 2:
        result = [2]
    else:
        return []
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i//2]:
            sieve[i*i // 2 ::i] = b'\x00'*len(sieve[i*i // 2 ::i])
    # Collect results
    result.extend([2*i + 3 for i in range(len(sieve)) if sieve[i]] [1:n//2 - 1 if n%2==0 else len(sieve)-1]
    return sorted(result)