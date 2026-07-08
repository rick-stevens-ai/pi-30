def fib(n: int) -> int:
    """Return the nth Fibonacci number using fast doubling (O(log n)).
    fib(0) = 0, fib(1) = 1.
    Works for arbitrarily large n using Python's exact integer arithmetic.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    # Inner recursive function returning (F(k), F(k+1))
    def _fib_pair(k: int) -> tuple[int, int]:
        if k == 0:
            return (0, 1)
        else:
            a, b = _fib_pair(k >> 1)
            c = a * ((b << 1) - a)          # F(2m) = F(m) * [2*F(m+1) – F(m)]
            d = a * a + b * b               # F(2m+1) = F(m)^2 + F(m+1)^2
            if k & 1:
                # k is odd: return (F(2m+1), F(2m+2))
                return (d, c + d)
            else:
                # k is even: return (F(2m), F(2m+1))
                return (c, d)
    return _fib_pair(n)[0]