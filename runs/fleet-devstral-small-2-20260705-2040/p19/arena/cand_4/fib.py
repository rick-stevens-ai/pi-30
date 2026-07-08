def fib(n: int) -> int:
    """Return the nth Fibonacci number using fast doubling method (O(log n)).
    
    Args:
        n: Non-negative integer index in Fibonacci sequence.
    
    Returns:
        The nth Fibonacci number as a Python bigint.
    
    Examples:
        >>> fib(0)
        0
        >>> fib(1)
        1
        >>> fib(5)
        5
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return _fib(n)[0]


def _fib(n: int) -> tuple[int, int]:
    """Helper function that returns (fib(n), fib(n+1))."""
    if n == 0:
        return (0, 1)
    a, b = _fib(n >> 1)
    c = a * (2 * b - a)
    d = a * a + b * b
    if n & 1:
        return (d, c + d)
    else:
        return (c, d)


if __name__ == "__main__":
    import time
    n = 200000
    start = time.time()
    result = fib(n)
    elapsed = time.time() - start
    print(f"fib({n}) = {result}")
    print(f"Time: {elapsed:.6f} seconds")