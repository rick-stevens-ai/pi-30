"""Fast-doubling Fibonacci with exact Python bigints.

Uses the identities:
    fib(2k)   = fib(k) * (2*fib(k+1) - fib(k))
    fib(2k+1) = fib(k)^2 + fib(k+1)^2

Recursion depth is O(log n); no memoization needed.
"""


def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1).

    Runs in O(log n) using fast doubling on Python's native arbitrary-precision
    integers.  Works correctly for any non-negative integer n.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    def _pair(k):
        # Returns (fib(k), fib(k+1)) via fast doubling.
        a, b = 0, 1
        for bit in reversed(bin(k)[3:]):          # skip "0b" and leading "0"
            if bit == '0':                         # k -> 2k
                c = a * (2 * b - a)               # fib(2m)
                d = a * a + b * b                  # fib(2m+1)
                a, b = c, d
            else:                                  # k -> 2k+1
                c = a * (2 * b - a)                # fib(2m)
                d = a * a + b * b                  # fib(2m+1)
                a, b = d, c + d                    # fib(2m+1), fib(2m+2)
        return a, b

    return _pair(n)[0]


if __name__ == "__main__":
    for n in (0, 1, 5, 10, 100):
        print(f"fib({n}) = {fib(n)}")
    # Quick sanity check at a large index
    import time
    t0 = time.time()
    val = fib(200_000)
    dt = time.time() - t0
    print(f"\nfib(200000) has {len(str(val))} digits, computed in {dt:.3f}s")
