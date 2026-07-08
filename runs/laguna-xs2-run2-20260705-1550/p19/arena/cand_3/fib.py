"""Fast Fibonacci using fast-doubling method, O(log n)."""

from typing import Tuple


def _fib_pair(n: int) -> Tuple[int, int]:
    """Return (F(n), F(n+1)) using fast doubling (iterative)."""
    if n == 0:
        return (0, 1)
    
    # Start with (F(0), F(1)) = (0, 1)
    # Process all bits of n to build up to (F(n), F(n+1))
    result: Tuple[int, int] = (0, 1)
    
    # Process each bit of n from MSB to LSB
    bits = bin(n)[2:]  # binary representation without '0b'
    
    for bit in bits:
        a, b = result
        # Doubling formulas:
        # F(2k) = F(k) * (2*F(k+1) - F(k))
        # F(2k+1) = F(k+1)^2 + F(k)^2
        c = a * (2 * b - a)  # F(2k)
        d = a * a + b * b    # F(2k+1)
        
        if bit == '0':
            # Current result is (F(k), F(k+1)), want (F(2k), F(2k+1))
            result = (c, d)
        else:
            # Current result is (F(k), F(k+1)), want (F(2k+1), F(2k+2))
            # F(2k+2) = F(2k+1) + F(2k) = d + c
            result = (d, d + c)
    
    return result


def fib(n: int) -> int:
    """Return the nth Fibonacci number.
    
    Uses fast-doubling algorithm for O(log n) time complexity.
    Uses Python's arbitrary precision integers (exact).
    
    >>> fib(0)
    0
    >>> fib(1)
    1
    >>> fib(10)
    55
    >>> fib(50)
    12586269025
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return _fib_pair(n)[0]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        print(fib(n))
    else:
        # Quick verification
        for i in range(20):
            print(f"fib({i}) = {fib(i)}")