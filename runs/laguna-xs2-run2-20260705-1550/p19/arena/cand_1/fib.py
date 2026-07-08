"""
Fast Fibonacci using fast-doubling method.
O(log n) time complexity, exact Python big integers.
"""

def fib(n: int) -> int:
    """
    Return the nth Fibonacci number using fast-doubling.
    fib(0) = 0, fib(1) = 1
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1

    def _fib_pair(k: int):
        """
        Return (F(k), F(k+1)) using fast-doubling recurrence.
        """
        if k == 0:
            return (0, 1)
        a, b = _fib_pair(k >> 1)
        # a = F(k'), b = F(k'+1) where k' = k // 2
        # F(2k') = F(k') * (2*F(k'+1) - F(k'))
        # F(2k'+1) = F(k')^2 + F(k'+1)^2
        c = a * ((b << 1) - a)  # F(2k')
        d = a * a + b * b        # F(2k'+1)
        if k & 1:
            return (d, c + d)    # k is odd: return (F(2k'+1), F(2k'+2))
        else:
            return (c, d)        # k is even: return (F(2k'), F(2k'+1))

    return _fib_pair(n)[0]