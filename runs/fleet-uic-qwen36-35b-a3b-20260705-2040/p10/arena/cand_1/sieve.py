"""Sieve of Eratosthenes — odd-only bytecode mark & slice-assign.

Key design (the "Candidate #1" angle):
  • We only store ODD candidates, so index *k* maps to candidate number k*k+2*k+3 = 2k+3.
  • A bytearray of bits: ``True`` → still prime, ``False`` → composite.
  • The inner cross-off is a single slice assignment — no Python loops in the hot path.
"""

from __future__ import annotations

__all__ = ("primes_up_to",)


def primes_up_to(n: int) -> list[int]:
    if n < 2:
        return []

    # ── small shortcut: we need every odd number up to ``n`` ──────────────
    limit = n - 1 >> 1          # how many odds (and thus bytes) we must track
    sieve = bytearray(b"\xff") * limit   # all-True: every odd is prime initially

    root = int((n - 3) ** 0.5 >> 1 + 1)  # last i with 2i+3 ≤ √n  (safe upper bound)

    for i in range(root):
        if sieve[i]:
            num = 2 * i + 3      # map back: i=0→3, i=1→5, …
            stride = 2 * num     # step size (only land on odd multiples)

            # first composite in our odd-only view to cross off:
            #    num² − 3  → divided by 2 gives the starting index under our mapping.
            start = (num * num - 3) >> 1
            sieve[start::stride] = b"\x00" * ((limit - start - 1) // stride + 1)

    # recover: emit "2", then every odd whose byte is still set
    return [2, *[2 * k + 3 for k, bit in enumerate(sieve) if bit]]


if __name__ == "__main__":
    import time

    for n in (10, 19, 100_000, 2_000_000):
        t0 = time.perf_counter()
        p = primes_up_to(n)
        dt = time.perf_counter() - t0
        print(f"primes ≤ {n:>9d}: {len(p)}  ({dt*1000:.2f} ms)")
