"""
Sieve of Eratosthenes – candidate #2 (odd-only sieve with slice assignment).

Stores only odd numbers in the bytearray, cutting memory in half.
Uses Python slice assignment (s[start::step] = ...) for bulk marking,
which pushes the inner loop into C and avoids Python-level iteration.
"""

from __future__ import annotations

def primes_up_to(n: int) -> list[int]:
    """Return a sorted list of all primes ≤ *n*.

    Correct for n < 2 (returns []), handles every edge case, and is
    fast at n = 2_000_000 thanks to:
      • odd-only bytearray (half the memory)
      • slice-assignment bulk marking (C-speed inner loop)
    """
    if n < 2:
        return []

    # Index i in `sieve` represents odd number 2*i + 1.
    # We need indices up to (n - 1) // 2 for the largest odd ≤ n.
    limit = (n - 1) // 2
    sieve: bytearray = bytearray(b'\x01') * (limit + 1)  # 1 = prime candidate

    # Mark composites.  Iterate only over odd bases p where p*p <= n.
    # For base p = 2*i + 1, its square is (2*i+1)^2 = 4*i^2 + 4*i + 1,
    # which maps to sieve index 2*i^2 + 2*i.  The step between consecutive
    # odd multiples of p is p (in sieve-index space, that's p).
    for i in range(1, int(limit**0.5) + 1):
        if sieve[i]:
            p = 2 * i + 1                     # the actual prime value
            start = 2 * i * (i + 1)           # sieve index of p*p
            sieve[start : limit + 1 : p] = b'\x00' * len(sieve[start : limit + 1 : p])

    # Reconstruct: 2 is always prime (when n >= 2), then collect odd primes.
    result = [2] if n >= 2 else []
    for i in range(1, limit + 1):
        if sieve[i]:
            result.append(2 * i + 1)

    return result


if __name__ == "__main__":
    import sys, time

    target = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000

    t0 = time.perf_counter()
    primes = primes_up_to(target)
    elapsed = time.perf_counter() - t0

    print(f"primes_up_to({target})  →  {len(primes)} primes  ({elapsed:.3f}s)")
    if target <= 100:
        print(f"  first few: {primes[:15]}")
        print(f"  last few:  {primes[-5:]}")
