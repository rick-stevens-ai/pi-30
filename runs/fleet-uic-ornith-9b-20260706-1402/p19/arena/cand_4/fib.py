def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1) using fast doubling."""

    def _helper(k):
        if k == 0:
            return (0, 1)
        a, b = _helper(k >> 1)
        c = a * ((b << 1) - a)           # F(2k)
        d = a * a + b * b                # F(2k+1)
        if k & 1:
            return (d, c + d)            # odd index -> shift up one step
        else:
            return (c, d)                # even index

    a, _ = _helper(n)
    return a
