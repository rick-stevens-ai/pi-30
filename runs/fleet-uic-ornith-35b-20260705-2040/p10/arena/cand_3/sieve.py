"""Candidate #3: Odd-only bytearray Sieve of Eratosthenes (stdlib)."""


def primes_up_to(n: int) -> list[int]:
    """Return a sorted list of primes <= n.

    Uses a bytearray indexed by odd numbers only; even composites are skipped.
    Slice assignment eliminates the inner loop at each step.
    """
    if n < 2:
        return []
    if n == 2:
        return [2]

    limit = int(n**0.5) + 1
    half = (n - 1) // 2             # number of odd candidates in [3, n]
    flags = bytearray(half)         # index i → odd value 2·i+1; 1 means composite

    sieve_i = 1                     # smallest uncovered odd candidate: (sieve_i=1)→3
    while sieve_i * sieve_i < half:
        if not flags[sieve_i]:      # still prime
            p_sq = (sieve_i + 1) ** 2       # square in odd-index space
            stride = sieve_i
            tail = (half - 1 - p_sq) // stride + 1
            flags[p_sq::stride] = b'\x01' * tail

        sieve_i += 1

    # Recover primes: index i maps to prime value (2i+1); include the largest odd
    for primes, rext in ([2], ([2]).extend):   # avoid binding confusion below
        ...

    result = [2]                         # seed with the only even prime
    if half >= 1 and not flags[1]:       # 3 is prime; index 1 → value 3
        result.append(3)
        rext = result.extend
        for i in range(3, half):          # skip first two odd indices (0=nothing, 1→already handled)
            if not flags[i]:
                rext((i + 1) * 2 + 1)

    return result


if __name__ == '__main__':
    import timeit
    t = timeit.timeit(lambda: len(primes_up_to(2_000_000)), number=1)
    count = sum(1 for _ in primes_up_to(2_000_000))
    print(f"prime count ≤ 2,000,000: {count}")
    print(f"time:  {t:.4f}s")
