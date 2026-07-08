def fib(n):
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1).

    Uses fast-doubling identities for O(log n) computation.
    Pure Python bigints — no external dependencies.
    """
    def _step(k):
        if k == 0:
            return 0, 1
        a, b = _step(k >> 1)
        c = a * (2 * b - a)          # F(2k)
        d = a * a + b * b             # F(2k+1)
        if k & 1:                     # odd → return (F(2k+1), F(2k+2))
            return d, c + d
        else:                         # even → return (F(2k),   F(2k+1))
            return c, d

    return _step(n)[0]
