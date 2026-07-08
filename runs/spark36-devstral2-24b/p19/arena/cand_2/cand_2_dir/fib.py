def fib(n: int) -> int:
    """
    Return the nth Fibonacci number using the fast doubling method.
    Uses exact Python bigint arithmetic.

    The Fibonacci sequence is defined as:
        fib(0) = 0
        fib(1) = 1
        fib(n) = fib(n-1) + fib(n-2) for n > 1

    The fast doubling method computes F(2k) and F(2k+1) in O(log n) time.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    def _fib_helper(m: int) -> tuple[int, int]:
        """Return (F(m), F(m+1))."""
        if m == 0:
            return (0, 1)
        a, b = _fib_helper(m >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        if m & 1:
            return (d, c + d)
        else:
            return (c, d)

    return _fib_helper(n)[0]
