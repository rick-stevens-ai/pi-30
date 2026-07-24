"""Fast Fibonacci via iterative fast-doubling — O(log n) exact bigints.

fib(0) = 0, fib(1) = 1.  Stdlib only.

The algorithm scans the bits of *n* from MSB to LSB, maintaining
the pair (F(k), F(k+1)) and applying the fast-doubling identities:

    F(2k)   = F(k) * (2*F(k+1) − F(k))
    F(2k+1) = F(k)^2 + F(k+1)^2

This is the *iterative* variant (no recursion, no matrix objects),
which avoids Python call overhead and stack limits — a distinct
angle from the more commonly seen recursive fast-doubling.
"""


def fib(n: int) -> int:
    """Return the *n*-th Fibonacci number (fib(0)=0, fib(1)=1).

    Uses iterative fast-doubling with bit scanning — O(log n) big-int
    multiplications, no recursion, no matrix objects.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0

    # (a, b) = (F(k), F(k+1)); start at k = 0.
    a, b = 0, 1

    # Scan bits of n from most-significant to least-significant.
    for i in range(n.bit_length() - 1, -1, -1):
        # Doubling step: (F(k), F(k+1)) → (F(2k), F(2k+1))
        c = a * ((b << 1) - a)      # F(2k)
        d = a * a + b * b           # F(2k+1)
        a, b = c, d

        # If bit i of n is set, advance k → k+1.
        if (n >> i) & 1:
            a, b = b, a + b

    return a


if __name__ == "__main__":
    import sys, time

    # --- quick self-test on small values ---
    _expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    for _i, _v in enumerate(_expected):
        assert fib(_i) == _v, f"fib({_i}) = {fib(_i)}, expected {_v}"

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000

    t0 = time.perf_counter()
    result = fib(n)
    elapsed = time.perf_counter() - t0

    if n <= 100:
        print(f"fib({n}) = {result}")
    else:
        print(f"fib({n}) has {len(str(result))} digits")
    print(f"computed in {elapsed:.4f}s")