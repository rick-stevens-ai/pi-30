# P23 SEED: improved sieve implementation.
def count_primes(n):
    """Count the number of primes strictly less than ``n`` using an
    efficient bytearray based Sieve of Eratosthenes which skips evens.

    The implementation mirrors the reference sieve in :mod:`check`, but it
    pre‑marks even numbers > 2 and iterates only over odd candidates, which
    gives a noticeable speed improvement while keeping full correctness.
    """
    if n <= 2:
        return 0

    sieve = bytearray([1]) * n
    sieve[0] = 0
    sieve[1] = 0

    # Mark all even numbers > 2 as composite.
    if n >= 4:
        sieve[4:n:2] = bytearray(len(sieve[4:n:2]))

    i = 3
    limit = int(n**0.5)
    while i <= limit:
        if sieve[i]:
            step = i * 2
            start = i * i
            sieve[start:n:step] = bytearray(len(sieve[start:n:step]))
        i += 2

    return sum(sieve)