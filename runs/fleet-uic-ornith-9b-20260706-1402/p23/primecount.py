# Sieve of Eratosthenes with bytearray, skip evens.
def count_primes(n):
    if n <= 2: return 0

    # Index i represents odd number (2*i + 1), starting from 1.
    sieve_size = n // 2
    sieve = bytearray([1]) * sieve_size
    if sieve_size > 0:
        sieve[0] = 0

    for i in range(1, sieve_size):
        num = 2 * i + 1
        if num * num >= n: break
        if sieve[i]:
            start_idx = (num * num - 1) // 2
            step = num
            mark_len = len(sieve[start_idx:sieve_size:step])
            if mark_len > 0:
                sieve[start_idx:sieve_size:step] = bytearray(mark_len)

    return min(1 + sum(sieve), n - 1)
