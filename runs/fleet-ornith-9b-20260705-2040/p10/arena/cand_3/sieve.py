def primes_up_to(n):
    """Return sorted list of primes <= n using Sieve of Eratosthenes.

    Uses bytearray + skip-evens trick for speed at large n.
    Stdlib only.

    Candidate #3: slice-assign odd-multiple marking on a compact sieve.
    """
    if n < 2:
        return []

    # Sieve over odd numbers only: index j represents candidate 2*j+1.
    # Only include indices where 2*j+1 <= n, so j < (n-1)//2 + 1.
    limit = (n - 1) // 2 + 1
    sieve = bytearray(limit)          # all zeros => "possibly prime"
    sieve[0] = 1                       # 1 is not prime

    # Only need to cross out multiples of primes up to sqrt(n).
    i = 3
    while (i * i) <= n:
        if sieve[i // 2] == 0:         # i is prime; mark its odd multiples.
            # Start marking at i*i, stepping by 2*i (skip evens).
            start_idx = i * i // 2     # index for i*i in the odd-only array
            step = i                   # stride between odd multiples of i
            sieve[start_idx::step] = b'\x01' * len(sieve[start_idx::step])
        i += 2

    # Collect primes: 2 plus all odd numbers whose entry is still 0.
    return [2] + [2 * j + 1 for j in range(1, limit) if sieve[j] == 0]
