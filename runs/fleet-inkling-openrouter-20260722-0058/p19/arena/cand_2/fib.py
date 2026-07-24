def fib(n):
    """Return the nth Fibonacci number using fast doubling. O(log n) bigints."""
    def _fib(k):
        if k == 0:
            return (0, 1)
        a, b = _fib(k >> 1)
        c = a * ((b << 1) - a)
        d = a * a + b * b
        if k & 1:
            return (d, c + d)
        return (c, d)
    return _fib(n)[0]
