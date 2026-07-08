def fib(n):
    """Return the nth Fibonacci number using fast doubling (O(log n)).

    Args:
        n: Non-negative integer index.

    Returns:
        The nth Fibonacci number as a Python int (bigint).
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    def _fib_pair(k):
        """Return (F(k), F(k+1)) via fast doubling."""
        if k == 0:
            return (0, 1)
        a, b = _fib_pair(k >> 1)
        c = a * ((b << 1) - a)
        d = a * a + b * b
        if k & 1:
            return (d, c + d)
        else:
            return (c, d)

    return _fib_pair(n)[0]


if __name__ == "__main__":
    # Simple sanity checks
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(10) == 55
    assert fib(20) == 6765
    # Large test (should be fast)
    print("fib(200000) length:", len(str(fib(200000))))