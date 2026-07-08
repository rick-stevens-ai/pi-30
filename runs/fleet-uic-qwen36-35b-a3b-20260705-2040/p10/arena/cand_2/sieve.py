"""Sieve of Eratosthenes — Candidate #2: bytearray + odd-only index mapping."""
from __future__ import annotations


def primes_up_to(n: int) -> list[int]:
    """Return a sorted list of all primes <= n.

  Fast path via `bytearray`, odd-index compression, and slice ``is`` assignment.
  Returns [] for every n < 2 (including negatives, zero, one).
    """
    if n < 2:
        return []

    # ── even-skip index mapping ────────────────────────────────
    # Index i represents the odd number (2*i + 3):   0→3, 1→5, 2→7, …
    size = (n - 1) >> 1                       # count of odd slots [3 .. n]

    sieve = bytearray(size)

    for i in range(len(sieve)):
        v = 2 * i + 3
        if v * v > n:                                     # stop when √n reached
            break
        if not sieve[i]:
            start = (v * v - 3) >> 1
            sieve[start::v] = b'\x01' * ((size - 1 - start) // v + 1)

    # Prime 2, then every compressed odd > 2 still marked 0
    result: list[int] = [2] if n >= 2 else []
    return result + [i * 2 + 3 for i, b in enumerate(sieve) if not b]


# Quick self-test ----------------------------------------------------
if __name__ == "__main__":
    def _check() -> None:
        from math import isqrt

        # Known anchors
        assert primes_up_to(0) == []
        assert primes_up_to(1) == []
        assert primes_up_to(2) == [2]
        assert primes_up_to(3) == [2, 3]
        assert primes_up_to(4) == [2, 3]
        assert primes_up_to(5) == [2, 3, 5]

        # Prime-count sanity (π(n))
        counts: list[tuple[int, int]] = [
            (10, 4), (25, 9), (100, 25), (7919 + 1, 1000)
        ]
        for n, expected in counts:
            got = len(primes_up_to(n))
            assert got == expected, f"π({n}): expected {expected}, got {got}"

    _check()
    print("All checks passed.")
