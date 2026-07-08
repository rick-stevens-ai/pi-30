"""
Fast Fibonacci function using the fast doubling method.
Returns the exact nth Fibonacci number as a Python bigint.
"""

def _fast_doubling_fib(n: int) -> tuple[int, int]:
    """Returns (fib(n), fib(n+1)) using the fast doubling method."""
    if n == 0:
        return (0, 1)
    a, b = _fast_doubling_fib(n >> 1)
    c = a * (2 * b - a)
    d = a * a + b * b
    if n & 1:
        return (d, c + d)
    else:
        return (c, d)


def fib(n: int) -> int:
    """
    Return the exact nth Fibonacci number using the fast doubling method.
    
    fib(0) = 0 and fib(1) = 1 by definition.
    Time complexity is O(log n), so it is fast even for large values like n=200000.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    return _fast_doubling_fib(n)[0]
