"""Fast Fibonacci using fast-doubling algorithm, O(log n)."""


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

    def _fib_pair(k: int):
        """Return (F(k), F(k+1)) using fast-doubling."""
        if k == 0:
            return (0, 1)
        a, b = _fib_pair(k >> 1)  # F(k/2), F(k/2 + 1)
        c = a * (2 * b - a)       # F(2k) = F(k) * (2*F(k+1) - F(k))
        d = a * a + b * b         # F(2k+1) = F(k)^2 + F(k+1)^2
        if k & 1:                 # odd: n = 2k + 1
            return (d, c + d)     # F(2k+1), F(2k+2)
        else:                     # even: n = 2k
            return (c, d)         # F(2k), F(2k+1)

    return _fib_pair(n)[0]