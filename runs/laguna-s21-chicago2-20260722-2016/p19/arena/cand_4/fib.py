"""Fast Fibonacci via iterative fast-doubling — O(log n).

fib(0) = 0, fib(1) = 1.
Exact Python big-int arithmetic, stdlib only.
Negative n supported via fib(-n) = (-1)^(n+1) * fib(n).

The algorithm scans the bits of |n| from MSB to LSB, maintaining the
invariant (a, b) = (fib(k), fib(k+1)).  Each bit triggers a "double"
step (k → 2k) and, if the bit is set, a "+1" step (2k → 2k+1).

Doubling identities (fast-doubling):
    fib(2k)   = fib(k) * (2*fib(k+1) - fib(k))
    fib(2k+1) = fib(k)^2 + fib(k+1)^2
"""

__all__ = ["fib"]


def fib(n: int) -> int:
    """Return the n-th Fibonacci number (fib(0)=0, fib(1)=1).

    Uses the fast-doubling recurrence, which runs in O(log n)
    big-integer operations.  Works for arbitrarily large n and
    supports negative indices.
    """
    if n == 0:
        return 0

    # Handle negative n: fib(-n) = (-1)^(n+1) * fib(n)
    if n < 0:
        n = -n
        sign = -1 if (n & 1) == 0 else 1
    else:
        sign = 1

    # Iterative fast-doubling over bits of |n|, MSB → LSB.
    # Invariant: (a, b) = (fib(k), fib(k+1)).
    a, b = 0, 1  # start at k = 0

    bit = 1 << (n.bit_length() - 1)  # highest set bit of |n|

    while bit:
        # --- Double step: (fib(k), fib(k+1)) → (fib(2k), fib(2k+1)) ---
        c = a * ((b << 1) - a)        # fib(2k)   = a*(2b - a)
        d = a * a + b * b             # fib(2k+1) = a^2 + b^2
        a, b = c, d

        # --- Conditional +1 step: (fib(2k), fib(2k+1)) → (fib(2k+1), fib(2k+2)) ---
        if n & bit:
            a, b = b, a + b

        bit >>= 1

    return sign * a


if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        t0 = time.perf_counter()
        result = fib(n)
        elapsed = time.perf_counter() - t0
        print(result)
        print(f"--- fib({n}) computed in {elapsed:.4f}s", file=sys.stderr)
    else:
        # Quick correctness check
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        for i, e in enumerate(expected):
            assert fib(i) == e, f"fib({i}) = {fib(i)}, expected {e}"
        # Negative indices
        assert fib(-1) == 1
        assert fib(-2) == -1
        assert fib(-3) == 2
        assert fib(-4) == -3
        print("All tests passed.")
        for i in range(20):
            print(f"fib({i}) = {fib(i)}")