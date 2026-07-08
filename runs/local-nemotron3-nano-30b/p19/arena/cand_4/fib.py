def fib(n: int) -> int:
    """
    Return the nth Fibonacci number using the fast‑doubling method.
    Runs in O(log n) time and uses Python's arbitrary-precision integers.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    def _fib(k):
        # returns (F(k), F(k+1))
        if k == 0:
            return (0, 1)
        else:
            a, b = _fib(k >> 1)
            # c = F(2m)   d = F(2m+1)
            c = a * ((b << 1) - a)          # F(2m)   = F(m) * (2*F(m+1) – F(m))
            d = a * a + b * b                # F(2m+1) = F(m)^2 + F(m+1)^2
            if k & 1:
                return (d, c + d)           # (F(2m+1), F(2m+2))
            else:
                return (c, d)               # (F(2m),   F(2m+1))

    return _fib(n)[0]


if __name__ == "__main__":
    # Simple sanity checks
    for i in range(10):
        print(i, fib(i))