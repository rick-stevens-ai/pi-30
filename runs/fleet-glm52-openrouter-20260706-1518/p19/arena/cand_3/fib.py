"""Fast Fibonacci via fast-doubling. O(log n) bigint, stdlib only."""


def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    # fast-doubling: F(2k) = F(k)*(2*F(k+1) - F(k))
    #                 F(2k+1) = F(k+1)^2 + F(k)^2
    def _fib(k: int) -> tuple[int, int]:
        if k == 0:
            return (0, 1)
        a, b = _fib(k >> 1)
        c = a * ((b << 1) - a)          # F(2m)
        d = a * a + b * b               # F(2m+1)
        if k & 1:
            return (d, c + d)
        return (c, d)

    return _fib(n)[0]


if __name__ == "__main__":
    import sys
    print(fib(int(sys.argv[1])))
