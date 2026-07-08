
def fib(n: int) -> int:
    """Return the n-th Fibonacci number with **exact** Python big‐int arithmetic.

    Uses fast doubling in O(log n) steps and recurses directly—no memo table, no cycles.
    Identites used:

        F(2k)   = F(k)[2·F(k+1) − F(k)]                (A)
        F(2k+1) = F(k)²  +  F(k+1)²                    (B)

    Base case: fib_pair(0) returns (F(0),F(1)) = (0,1).
    """

    def _pair(k: int):
        """Return the tuple ``(F(k), F(k+1))``."""
        if k == 0:
            return 0, 1
        a, b = _pair(k >> 1)              # m = k//2 → (F(m), F(m+1))
        c = a * ((b << 1) - a)             # F(2m)   by identity (A)
        d = a*a + b*b                      # F(2m+1) by identity (B)
        if k & 1:                          # odd
            return d, c + d                # (F(k),   F(k+1))
        else:                              # even
            return c, d                    # (F(k),   F(k+1))

    if n < 0:
        raise ValueError("n must be non-negative")
    return _pair(n)[0]


# ---------------------------------------------------------------------------
# Optional self-test / benchmark (execute this file directly)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys, time

    # small-value sanity check
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34,
                55, 89, 144, 233, 377, 610, 987,
                1597, 2584, 4181]
    for i in range(20):
        assert fib(i) == expected[i], f"fib({i})={fib(i)} != {expected[i]}"

    # large-value benchmark: n=200_000 (≈41 798 digits)
    sys.set_int_max_str_digits(50_000)          # needed for str(v) → len(...) printout
    t = time.perf_counter()
    v = fib(200_000)
    dt = time.perf_counter() - t
    print(f"fib(200_000):  {len(str(v))} digits, computed in {dt:.4f}s")
