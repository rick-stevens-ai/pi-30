def primes_up_to(n):
    if n < 2:
        return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    sieve[2] = 1
    # Mark even numbers > 2 as non-prime
    sieve[4::2] = b'\x00' * len(sieve[4::2])
    # Sieve for odd numbers
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i] == 1:
            sieve[i*i::i] = b'\x00' * len(sieve[i*i::i])
    # Collect primes
    return [i for i, is_prime in enumerate(sieve) if is_prime]