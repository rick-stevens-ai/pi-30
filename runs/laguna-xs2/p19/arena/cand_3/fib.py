"""Fast Fibonacci using fast-doubling algorithm, O(log n)."""


def fib(n: int) -> int:
    """Return the nth Fibonacci number.
    
    Uses fast-doubling algorithm for O(log n) time complexity.
    fib(0) = 0, fib(1) = 1.
    
    Args:
        n: Non-negative integer index
        
    Returns:
        The nth Fibonacci number as a Python int (bigint)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    return _fib_pair(n)[0]


def _fib_pair(n: int) -> tuple[int, int]:
    """Return (F(n), F(n+1)) using fast-doubling recurrence.
    
    Identities used:
        F(2k)   = F(k) * (2*F(k+1) - F(k))
        F(2k+1) = F(k)^2 + F(k+1)^2
    """
    if n == 0:
        return (0, 1)
    if n == 1:
        return (1, 1)
    
    a, b = _fib_pair(n >> 1)  # F(k), F(k+1) where k = n // 2
    
    # F(2k) = F(k) * (2*F(k+1) - F(k))
    # F(2k+1) = F(k)^2 + F(k+1)^2
    c = a * ((b << 1) - a)       # F(2k)
    d = a * a + b * b            # F(2k+1)
    
    if n & 1:
        return (d, c + d)        # F(2k+1), F(2k+2) = F(2k+1) + F(2k)
    else:
        return (c, d)            # F(2k), F(2k+1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        print(f"fib({n}) = {fib(n)}")