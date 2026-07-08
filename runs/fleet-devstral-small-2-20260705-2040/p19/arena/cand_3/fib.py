def fib(n: int) -> int:
    """Return the nth Fibonacci number using fast doubling method.
    
    Args:
        n: The index in the Fibonacci sequence (0-indexed).
    
    Returns:
        The nth Fibonacci number as an exact Python bigint.
    
    Examples:
        >>> fib(0)
        0
        >>> fib(1)
        1
        >>> fib(10)
        55
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return _fib(n)[0]


def _fib(n: int) -> tuple[int, int]:
    """Return (fib(n), fib(n+1)) using fast doubling.
    
    This is a helper function for the fast doubling method.
    """
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
    end = time.time()
    print(f"fib({n}) = {result}")
    print(f"Time taken: {end - start:.6f} seconds")