"""Fast Fibonacci using exact Python bigint with fast-doubling (O(log n))."""


def fib(n):
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1) using fast-doubling."""
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


if __name__ == "__main__":
    print(fib(200000))
