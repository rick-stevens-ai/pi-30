"""Fast-doubling Fibonacci. Exact Python int. O(log n). Stdlib only."""

def _fib_pair(n):
    """Return (F(n), F(n+1))."""
    if n == 0:
        return (0, 1)
    a, b = _fib_pair(n >> 1)
    c = a * ((b << 1) - a)
    d = a * a + b * b
    if n & 1:
        return (d, c + d)
    return (c, d)

def fib(n):
    return _fib_pair(n)[0]

if __name__ == "__main__":
    import sys, time
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    t = time.perf_counter()
    val = fib(n)
    t = time.perf_counter() - t
    print(f"fib({n}) has {len(str(val))} digits")
    print(f"time: {t:.4f}s")
