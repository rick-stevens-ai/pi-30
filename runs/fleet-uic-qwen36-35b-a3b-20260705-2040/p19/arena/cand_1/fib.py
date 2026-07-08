"""
Fast-doubling Fibonacci — O(log n) via exact Python bigint arithmetic.

Returns F(n) where F(0)=0, F(1)=1.
"""


def fib(n: int) -> int:
    """Return the nth Fibonacci number using fast doubling."""
    if n < 0:
        raise ValueError("n must be non-negative")

    def _fib_pair(k):
        """Return (F(k), F(k+1)) via fast doubling."""
        if k == 0:
            return (0, 1)
        a, b = _fib_pair(k >> 1)          # a = F(m), b = F(m+1), m = k//2
        c = a * ((b << 1) - a)             # F(2m)   = F(m)·[2F(m+1) − F(m)]
        d = a * a + b * b                   # F(2m+1) = F(m)² + F(m+1)²
        if k & 1:
            return (d, c + d)               # odd:  (F(2m+1), F(2m+2))
        else:
            return (c, d)                   # even: (F(2m),   F(2m+1))

    return _fib_pair(n)[0]


if __name__ == "__main__":
    import time

    for n in (10, 100, 1_000, 10_000, 50_000, 200_000):
        t0 = time.perf_counter()
        result = fib(n)
        elapsed = time.perf_counter() - t0
        # Print digit count as a proxy for size
        digits = len(str(result)) if result else 1
        print(f"fib({n:>7})  ->  {digits} digits  ({elapsed*1000:6.2f} ms)")
