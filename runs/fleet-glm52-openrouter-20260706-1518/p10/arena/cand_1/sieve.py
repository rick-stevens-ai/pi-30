"""Sieve of Eratosthenes: primes_up_to(n) -> sorted list of primes <= n.

Optimizations:
- bytearray sieve (one byte per odd candidate, not per integer)
- only odd numbers are tracked (evens except 2 are composite)
- slice assignment for fast bulk marking of multiples
- returns list[2] + odd primes directly in ascending order (already sorted)
"""

from typing import List


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of all primes <= n.

    Correct for all integer inputs:
      - n < 2          -> []
      - n == 2         -> [2]
      - n == 3         -> [2, 3]
      - larger n       -> full sorted prime list

    Args:
        n: inclusive upper bound (any int; negatives/treated < 2).

    Returns:
        Sorted list of primes <= n.
    """
    # Normalize / handle trivial cases. Handles floats-via-int, negatives, etc.
    if not isinstance(n, int) or isinstance(n, bool):
        # Be permissive for integer-like inputs but reject bools.
        raise TypeError("n must be an int")
    if n < 2:
        return []
    if n == 2:
        return [2]

    # Number of odd candidates: 1, 3, 5, ..., largest odd <= n.
    # Index i corresponds to the odd value v = 2*i + 1.
    # We want v <= n  =>  2*i + 1 <= n  =>  i <= (n - 1)//2.
    last = (n - 1) // 2  # index of largest odd <= n
    # sieve[i] == 1 means "composite"; 0 means "prime candidate".
    sieve = bytearray(last + 1)

    # Only need to strike multiples of odd primes p where p*p <= n.
    # p = 2*i + 1; p*p <= n  =>  i <= (isqrt(n) - 1)//2.
    # Use integer sqrt via math.isqrt (stdlib, exact).
    import math
    limit_val = math.isqrt(n)
    limit_i = (limit_val - 1) // 2

    for i in range(1, limit_i + 1):
        if sieve[i]:
            continue
        p = 2 * i + 1
        start = p * p
        # step by 2*p because p is odd: p*p, p*(p+2), ... are the odd multiples.
        # Convert each multiple m to index: m -> (m - 1)//2.
        # start index for value p*p:
        start_i = (start - 1) // 2
        # step in index space is p (since (m + 2p - 1)//2 - (m - 1)//2 = p).
        step = p
        # Slice assignment: mark [start_i : last+1 : step] as composite.
        sieve[start_i : last + 1 : step] = b"\x01" * (((last - start_i) // step) + 1)

    # Collect results: 2, then odd primes in order.
    out = [2]
    # Iterate over candidate indices; append value where sieve[i] == 0.
    # Use enumerate on the bytearray; values are ints 0/1.
    append = out.append
    for i, flag in enumerate(sieve):
        if i == 0:
            continue  # value 1, not prime
        if not flag:
            append(2 * i + 1)
    return out


if __name__ == "__main__":
    import sys

    def _self_test():
        # Basic correctness
        assert primes_up_to(-5) == []
        assert primes_up_to(0) == []
        assert primes_up_to(1) == []
        assert primes_up_to(2) == [2]
        assert primes_up_to(3) == [2, 3]
        assert primes_up_to(4) == [2, 3]
        assert primes_up_to(10) == [2, 3, 5, 7]
        assert primes_up_to(11) == [2, 3, 5, 7, 11]
        assert primes_up_to(13) == [2, 3, 5, 7, 11, 13]
        assert primes_up_to(25) == [2, 3, 5, 7, 11, 13, 17, 19, 23]
        assert primes_up_to(29) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        assert primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        # Boundary on even/odd n
        assert primes_up_to(2_000_000)[-1] == 1_999_993
        # Count check (known value): pi(2,000,000) = 148933
        assert len(primes_up_to(2_000_000)) == 148933
        # Sortedness
        big = primes_up_to(2_000_000)
        assert all(big[i] < big[i + 1] for i in range(len(big) - 1))
        print("self-test passed")

    if len(sys.argv) > 1 and sys.argv[1] == "bench":
        import time

        t0 = time.perf_counter()
        ps = primes_up_to(2_000_000)
        t1 = time.perf_counter()
        print(f"primes_up_to(2_000_000): {len(ps)} primes in {t1 - t0:.4f}s")
    else:
        _self_test()
