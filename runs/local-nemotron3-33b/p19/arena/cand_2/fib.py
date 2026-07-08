def fib(n: int) -> int:
    """
    Return the nth Fibonacci number (F(0)=0, F(1)=1).
    Uses the fast‑doubling algorithm with O(log n) time and exact Python ints.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    def _fib_pair(k: int):
        """Return (F(k), F(k+1)) using fast-doubling."""
        if k == 0:
            return 0, 1
        # Recursively compute for k // 2
        a, b = _fib_pair(k >> 1)          # a=F(m), b=F(m+1) where m=k//2
        # Apply doubling formulas
        c = a * ((b << 1) - a)            # F(2m) = F(m)*(2*F(m+1)-F(m))
        d = a * a + b * b                 # F(2m+1) = F(m)^2 + F(m+1)^2
        if k & 1:                         # k is odd
            return d, c + d               # (F(2m+1), F(2m+2))
        else:
            return c, d                   # (F(2m), F(2m+1))

    return _fib_pair(n)[0]


# Simple sanity checks (can be removed or commented out)
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        print(fib(n))
    else:
        # test a few values
        for i in range(10):
            print(i, fib(i))