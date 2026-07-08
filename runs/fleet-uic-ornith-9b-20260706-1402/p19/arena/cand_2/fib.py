def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1).

    Uses fast-doubling identities for O(log n) time with Python bigints.
    """
    def _pair(k):
        if k == 0:
            return 0, 1
        a, b = _pair(k >> 1)
        c = a * (2 * b - a)   # fib(2m)
        d = a * a + b * b     # fib(2m+1)
        if k & 1:
            return d, c + d   # fib(2m+1), fib(2m+2)
        else:
            return c, d       # fib(2m), fib(2m+1)

    return _pair(n)[0]
