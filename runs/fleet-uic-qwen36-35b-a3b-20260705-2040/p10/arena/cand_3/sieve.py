"""Sieve of Eratosthenes — candidate #3: odd-only bytearray with slice assign."""

import math


def primes_up_to(n: int) -> list[int]:
    """Return a sorted list of all prime numbers <= n.

    Uses a compact ``bytearray`` covering only the odd integers  (1, 3, …).
    Composite odds are crossed off via :meth:`bytearray.__setitem__` on
    stepped slices — fast C-level bulk assignment at n = 2 000 000.

    Index → value:  *i* ↔ (2 · i + 1) .
    Convention: ``sieve[i] == 0`` means "prime candidate", ``>0`` means
    "crossed off as composite".
    """
    # ---- trivial / edge cases ------------------------------------------------
    if n < 2:
        return []
    if n == 2:
        return [2]                      # fast-path (the lone even prime)

    half = (n - 1) // 2 + 1           # count of odd numbers in [0 … n]; sieve[i] covers value (2*i+1)
    sieve = bytearray(half)           # bytes.zeros initially → all candidates marked as "prime"

    limit = int(math.isqrt(n))        # cross-off multiples of odds ≤ √n

    for i in range(1, half):          # walk sieve indices; i=0 would be value 1
        if sieve[i]:                  # composite? skip.
            continue

        val = i + i + 1               # = 2*i + 1 (a prime!)

        if val > limit:
            break                     # no need to cross off more multiples

        idx0 = ((val * val) - 1) >> 1  # index of the first odd composite (val²)
        step_len = (half - 1 - idx0) // val + 1 if idx0 < half else 0
        sieve[idx0::val] = b'\x01' * step_len   # mark composites as non-zero

    return [2] + [(idx << 1 | 1) for idx, flag in enumerate(sieve) if not flag]
