"""Fast Fibonacci using fast-doubling method (O(log n))."""

def fib(n: int) -> int:
    """
    Return the nth Fibonacci number (fib(0)=0, fib(1)=1).
    
    Uses fast-doubling algorithm for O(log n) time complexity.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    def _fib_pair(k: int) -> tuple[int, int]:
        """Return (F(k), F(k+1)) using fast doubling."""
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
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    print(fib(n))