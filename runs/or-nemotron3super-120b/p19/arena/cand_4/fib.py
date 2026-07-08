def fib(n: int) -> int:
    """Return the nth Fibonacci number using fast doubling.
    fib(0) = 0, fib(1) = 1.
    Works for arbitrarily large n using Python's exact integers.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    # Fast doubling algorithm (recursive)
    def _fib(k: int) -> tuple[int, int]:
        if k == 0:
            return (0, 1)
        else:
            a, b = _fib(k // 2)
            c = a * ((b << 1) - a)          # c = F(2k)
            d = a * a + b * b               # d = F(2k+1)
            if k & 1:                       # k is odd
                return (d, c + d)
            else:                           # k is even
                return (c, d)
    return _fib(n)[0]


if __name__ == "__main__":
    # Simple self-test
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(10) == 55
    assert fib(50) == 12586269025
    # Large n test (should be fast)
    # print(fib(200000))  # Uncomment to see (large number)
    print("All tests passed.")