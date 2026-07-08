# P23 OPTIMISED: Sieve of Eratosthenes on odds only (bytearray)
def count_primes(n):
    if n <= 2:
        return 0
    half = (n - 1) // 2          # number of odd integers in [1, n)
    sieve = bytearray(b'\x01') * half   # index i represents odd number (2i+1)
    i = 1                             # iterate over bit indices starting from p=3 (=odd#1)
    while True:
        p = i + i + 1               # the odd prime candidate: 2i+1
        pp = p * p                    # smallest composite to start marking at (must be odd)
        if pp >= n:
            break
        s = pp >> 1                   # index of pp (= pp-1 // 2) for an odd number
        sieve[s::p] = b'\x00' * (((half - 1 - s) // p) + 1)
        i += 1

    sieve[0] = 0                    # index 0 = odd #1 is not prime
    return sum(sieve) + (n > 2)
