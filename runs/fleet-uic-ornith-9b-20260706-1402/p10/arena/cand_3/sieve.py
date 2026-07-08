"""
Candidate #3 — Odd-only Sieve of Eratosthenes with bytearray + slice assign.

Distinct angle vs other candidates:
  • Index-map odd numbers only (index i ↔ candidate 2i+1), so the sieve array
    contains exactly the odd primes ≥ 3 and nothing else.
  • Prime 2 is returned unconditionally from a separate slot — it's never in
    the sieve, so no mask/unmask logic needed for it.
  • Slice assign (`sieve[start::step] = b'\x00' * N`) clears entire runs of
    composite markers in one C-level memcpy, far faster than looping.

Edge cases: n < 2 → [] (empty), n == 2 → [2], n == 3 → [2, 3].
"""


def primes_up_to(n):
    if n < 2:
        return []
    if n == 2:
        return [2]

    # --- sieve array: bytearray, index i ↔ candidate (2i+1) ---
    size = (n + 1) // 2                 # covers all odd numbers ≤ n
    sieve = bytearray(b'\x01') * size   # all odd candidates start as prime

    limit_idx = int(n**0.5) // 2 + 1    # largest index whose candidate ≤ √n

    for i in range(3, min(limit_idx * 2 + 1, n), 2):
        idx = (i - 1) >> 1              # index of prime `i` inside the array
        if sieve[idx]:                  # only cross-sieve if still marked prime
            start = ((i * i) - 1) >> 1  # first odd multiple ≥ i², in index space
            step = i                    # stride between successive odd multiples
            # Skip marking entirely if the first composite is beyond our range.
            if start < size:
                count = (size - start + step - 1) // step
                sieve[start::step] = b'\x00' * count

    # --- collect result: always include 2, then scan the sieve for odds ---
    primes = [2]
    for idx in range(1, size):
        if sieve[idx]:
            primes.append(idx << 1 | 1)  # decode index back to number: 2i+1

    return primes


if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    p = primes_up_to(2_000_000)
    dt = time.perf_counter() - t0
    print(f"Found {len(p)} primes ≤ 2,000,000 in {dt:.4f}s")
    # Spot-check first/last and count
    assert p[0] == 2
    assert len(p) >= 148933  # known π(2_000_000) = 148933
    print(f"First: {p[0]}, Last: {p[-1]}")
