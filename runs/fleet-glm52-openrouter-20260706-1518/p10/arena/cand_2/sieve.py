"""Sieve of Eratosthenes optimized for large n (odd-only, bytearray, slice assign)."""

import math


def primes_up_to(n):
    """Return a sorted list of all primes <= n.

    Handles n < 2 (empty), n == 2, and large n efficiently using an
    odd-only bytearray sieve with slice assignment.
    """
    if n < 2:
        return []

    # 2 is the only even prime; handle it explicitly, then sieve odds only.
    # Map odd number k -> index (k >> 1). Index i represents k = 2*i + 1.
    # We only mark composites among odd numbers >= 3.
    if n == 2:
        return [2]

    limit = n + 1  # we want primes <= n
    # Number of odd candidates in [1, n]: (limit // 2)
    size = limit >> 1  # indices 0..size-1
    is_composite = bytearray(size)  # 0 = prime candidate, 1 = composite

    # Index 0 corresponds to 1 (not prime). Mark it composite.
    is_composite[0] = 1

    # For each odd prime p = 2*i + 1 with p*p <= n, mark multiples.
    # We start marking from p*p (smaller multiples already handled),
    # stepping by 2*p (skip even multiples) in number space.
    # In index space: start index = (p*p) >> 1, step = p.
    i = 1  # p = 3
    sqrt_n = int(math.isqrt(n))
    while True:
        p = (i << 1) | 1  # 2*i + 1
        if p > sqrt_n:
            break
        if not is_composite[i]:
            # p is prime; mark odd multiples p*p, p*p + 2p, ...
            start = (p * p) >> 1
            step = p
            # slice assignment for speed
            is_composite[start::step] = b"\x01" * (((size - start - 1) // step) + 1)
        i += 1

    # Collect results.
    primes = [2]
    # All odd indices i>=1 with is_composite[i]==0 are prime (k=2*i+1).
    # Build list comprehension over the bytes.
    primes.extend((i << 1) | 1 for i in range(1, size) if not is_composite[i])
    return primes


if __name__ == "__main__":
    # Quick sanity checks.
    assert primes_up_to(-5) == []
    assert primes_up_to(0) == []
    assert primes_up_to(1) == []
    assert primes_up_to(2) == [2]
    assert primes_up_to(3) == [2, 3]
    assert primes_up_to(10) == [2, 3, 5, 7]
    assert primes_up_to(11) == [2, 3, 5, 7, 11]
    assert primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert len(primes_up_to(100)) == 25
    import time

    t = time.time()
    ps = primes_up_to(2_000_000)
    dt = time.time() - t
    assert len(ps) == 148933, len(ps)
    assert ps[0] == 2 and ps[-1] == 1999993
    print(f"n=2,000,000 -> {len(ps)} primes in {dt:.3f}s")
    print("all checks passed")
