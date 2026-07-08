"""Sieve of Eratosthenes — bytearray + odd-only + slice‑assign variant."""

from __future__ import annotations

import math
from typing import List


def primes_up_to(n: int) -> List[int]:
    """Return a sorted list of all primes *p* with *p* ≤ *n*.

    Uses an odd‑only ``bytearray`` sieve and slice assignment to
    eliminate composite marks in bulk, which is noticeably faster
    than a per‑element loop for large *n* (e.g. 2 000 000).
    """
    if n < 2:
        return []

    # ------------------------------------------------------------------
    # Odd‑only sieve: index *i* represents the number 2*i + 3.
    #   i=0 -> 3,  i=1 -> 5,  i=2 -> 7,  …
    # We need indices for all odd numbers up to *n*.
    # ------------------------------------------------------------------
    size = (n - 1) // 2  # number of odd slots (last odd ≤ n is at index size-1)
    sieve: bytearray = bytearray([1]) * size  # 1 = "possibly prime"

    # We only need to sieve up to sqrt(n).
    # For each prime *p* (odd), the first multiple to cross out is p².
    # p² maps to index (p² - 3) // 2, step is p (skip every p-th odd).
    sqrt_n = int(math.isqrt(n))

    for i in range(size):
        if sieve[i]:
            p = 2 * i + 3  # actual prime value
            if p > sqrt_n:
                break
            # Mark multiples of p starting from p², stepping by 2p
            # (which is p steps through the odd-only array).
            start = (p * p - 3) // 2
            sieve[start::p] = b'\x00' * len(sieve[start::p])

    # ------------------------------------------------------------------
    # Collect results: always include 2, then every odd index still set.
    # ------------------------------------------------------------------
    result = [2]
    result.extend(2 * i + 3 for i, flag in enumerate(sieve) if flag)
    return result


# ------------------------------------------------------------------
# Quick smoke test when run directly
# ------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    def _check():
        assert primes_up_to(1) == []
        assert primes_up_to(2) == [2]
        assert primes_up_to(3) == [2, 3]
        assert primes_up_to(10) == [2, 3, 5, 7]
        assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
        assert primes_up_to(0) == []
        assert primes_up_to(-5) == []

        # Larger check — known count for n=1_000_000 is 78 498
        big = primes_up_to(1_000_000)
        assert len(big) == 78_498, f"expected 78498, got {len(big)}"
        assert big[0] == 2
        assert big[-1] == 999_983  # largest prime ≤ 1_000_000

        # Performance sanity: n=2_000_000 should run in < 1 sec
        import time
        t0 = time.perf_counter()
        big2 = primes_up_to(2_000_000)
        elapsed = time.perf_counter() - t0
        assert len(big2) == 148_933, f"expected 148933, got {len(big2)}"
        print(f"primes_up_to(2_000_000) → {len(big2)} primes in {elapsed:.3f}s", file=sys.stderr)

        print("All checks passed.", file=sys.stderr)

    _check()
