"""
Fast Fibonacci using fast-doubling algorithm.
O(log n) time complexity, exact Python bigint arithmetic.
"""


def fib(n: int) -> int:
    """Return the nth Fibonacci number.

    Uses fast-doubling algorithm for O(log n) time complexity.
    fib(0) = 0, fib(1) = 1, fib(2) = 1, fib(3) = 2, ...

    Args:
        n: Non-negative integer index

    Returns:
        The nth Fibonacci number as a Python int (bigint)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0

    def _fib_pair(k: int):
        """Return (F(k), F(k+1)) using fast-doubling recursion."""
        if k == 0:
            return (0, 1)
        a, b = _fib_pair(k >> 1)  # F(k//2), F(k//2 + 1)
        # Fast-doubling formulas:
        # F(2k)   = F(k) * (2*F(k+1) - F(k))
        # F(2k+1) = F(k)^2 + F(k+1)^2
        c = a * ((b << 1) - a)   # F(2k)
        d = a * a + b * b        # F(2k+1)
        if k & 1:
            return (d, c + d)    # (F(2k+1), F(2k+2))
        else:
            return (c, d)        # (F(2k), F(2k+1))

    return _fib_pair(n)[0]


if __name__ == "__main__":
    # Quick verification
    for i in range(10):
        print(f"fib({i}) = {fib(i)}")
    print(f"fib(200000) has {len(str(fib(200000)))} digits")