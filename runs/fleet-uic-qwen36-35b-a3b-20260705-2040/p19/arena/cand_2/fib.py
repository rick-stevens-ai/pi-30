"""Fast-doubling Fibonacci — O(log n) exact Python bigints, stdlib only."""


def fib(n: int) -> int:
    """Return the *n*-th Fibonacci number (fib(0)=0, fib(1)=1).

    Uses the fast-doubling identities:

        F(2k)   = F(k)·[2·F(k+1) − F(k)]
        F(2k+1) = F(k)² + F(k+1)²

     Each call halves *n*, giving Θ(log n) arithmetic steps on Python's
    arbitrary-precision integers.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    def _fib_pair(k):
        # Returns (F(k), F(k+1)) recursively by halving k.
        if k == 0:
            return (0, 1)
        fk, fkpp1 = _fib_pair(k >> 1)          # (F(m), F(m+1)), m = k//2
        c = fk * ((fkpp1 << 1) - fk)            # F(2m)
        d = fk * fk + fkpp1 * fkpp1             # F(2m+1)
        if k & 1:                                # odd → shift one step
            return (d, c + d)                    # (F(2m+1), F(2m+2))
        else:                                    # even
            return (c, d)                        # (F(2m),   F(2m+1))

    return _fib_pair(n)[0]


# --- lightweight self-test only when run directly -------------------------
if __name__ == "__main__":
    import time

    # Correctness spot-checks
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(10) == 55
    assert fib(100) == 354224848179261915075

    # Scale test — n=200 000 (≈ 41 797 digits) should finish in a flash.
    t0 = time.perf_counter()
    result = fib(200_000)
    elapsed = time.perf_counter() - t0

    print(f"fib(200_000): {len(str(result))} digits  [{elapsed:.4f}s]")
    assert len(str(result)) == 41_798   # known digit count for F(200_000)
    print("All checks passed.")
