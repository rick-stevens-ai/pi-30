def primes_up_to(n):
    """Return sorted list of all primes less than or equal to n."""
    if n < 2:
        return []
    
    if n == 2:
        return [2]
    
    # Sieve for odd numbers only: index i represents 2*i + 3
    # i.e., 3, 5, 7, 9, ...
    limit = (n - 1) // 2
    is_prime = bytearray(b'\x01') * limit
    
    sqrt_n = int(n ** 0.5)
    
    for i in range((sqrt_n - 1) // 2):
        if is_prime[i]:
            p = 2 * i + 3
            start = (p * p - 3) // 2
            # Mark multiples of p starting from p^2
            is_prime[start::p] = b'\x00' * ((limit - start + p - 1) // p)
    
    return [2] + [2 * i + 3 for i in range(limit) if is_prime[i]]