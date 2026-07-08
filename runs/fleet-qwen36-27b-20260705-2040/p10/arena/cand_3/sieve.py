"""
Sieve of Eratosthenes — odd-only bytearray with slice-assign marking.

Distinct angle (cand_3): stores only odd candidates in a bytearray,
uses Python slice assignment (the fastest bulk-write primitive) to
cross out multiples in one shot, and reconstructs the result list
with a single list comprehension.
"""

from __future__ import annotations

def primes_up_to(n: int) -> list[int]:
    """Return a sorted list of all primes ≤ *n*.

    Uses an odd-only ``bytearray`` so that half the memory is saved
    and slice-assignment can cross out every other multiple in one
    C-level call.

    Examples
    --------
    >>> primes_up_to(10)
    [2, 3, 5, 7]
    >>> primes_up_to(1)
    []
    >>> primes_up_to(2)
    [2]
    """
    if n < 2:
        return []

    # ------------------------------------------------------------------
    # Layout: index i in `sift` represents the odd number 2*i + 1.
    #         sif[i] == 1 means "still a candidate" (prime or unknown).
    #         sif[i] == 0 means "composite — crossed out".
    # ------------------------------------------------------------------
    size = (n + 1) >> 1                      # number of odd integers in [1..n]
    sift = bytearray([1]) * size              # all odds start as candidates

    limit = int(n**0.5)                       # only need to sieve up to sqrt(n)

    for p in range(3, limit + 1, 2):
        if sift[p >> 1]:                      # p is still prime
            # First composite of p is p*p; its index is (p*p) >> 1.
            # Step is 2*p (skip even multiples), so stride in indices is p.
            start = (p * p) >> 1
            stride = p
            sift[start : size : stride] = b'\x00' * ((size - start + stride - 1) // stride)

    # ------------------------------------------------------------------
    # Reconstruct: 2 is always prime for n >= 2, then collect surviving odds.
    # ------------------------------------------------------------------
    return [2] + [2 * i + 1 for i, flag in enumerate(sift) if i and flag]


# ------------------------------------------------------------------
# Quick self-test when run as a script.
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Correctness smoke-tests
    assert primes_up_to(0) == []
    assert primes_up_to(1) == []
    assert primes_up_to(2) == [2]
    assert primes_up_to(3) == [2, 3]
    assert primes_up_to(10) == [2, 3, 5, 7]
    assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    assert primes_up_to(100)[-1] == 97
    assert len(primes_up_to(100)) == 25

    # Performance sanity-check
    import time
    t0 = time.perf_counter()
    p2m = primes_up_to(2_000_000)
    t1 = time.perf_counter()
    print(f"primes_up_to(2_000_000) → {len(p2m)} primes  ({t1 - t0:.3f}s)")
    assert len(p2m) == 148_933
    assert p2m[0] == 2
    assert p2m[-1] == 1_999_993
    print("All checks passed.")
