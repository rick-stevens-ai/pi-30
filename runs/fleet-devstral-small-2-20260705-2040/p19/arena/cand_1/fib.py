def fib(n: int) -> int:
    """Return the nth Fibonacci number using fast doubling method.
    
    Args:
        n: The index in the Fibonacci sequence (0-based).
    
    Returns:
        The nth Fibonacci number as an exact Python bigint.
    
    Examples:
        fib(0) -> 0
        fib(1) -> 1
        fib(2) -> 1
        fib(3) -> 2
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return _fib(n)[0]


def _fib(n: int) -> tuple[int, int]:
    """Helper function for fast doubling method.
    
    Returns:
        A tuple (F(n), F(n+1)) where F(n) is the nth Fibonacci number.
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