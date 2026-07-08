"""Fast Fibonacci using fast-doubling algorithm. O(log n) time, exact Python bigint."""

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
    
    # Iterative fast-doubling: work from MSB to LSB of n
    # Build up (F(k), F(k+1)) for k being the bits of n seen so far
    def fib_pair(k: int) -> tuple[int, int]:
        """Return (F(k), F(k+1)) using iterative fast doubling."""
        # Find highest bit position
        bits = k.bit_length()
        a, b = 0, 1  # F(0), F(1)
        for i in range(bits - 1, -1, -1):
            # Fast-doubling formulas:
            # F(2n) = F(n) * [2*F(n+1) - F(n)]
            # F(2n+1) = F(n+1)^2 + F(n)^2
            c = a * (2 * b - a)
            d = a * a + b * b
            if (k >> i) & 1:
                a, b = d, c + d  # F(2n+1), F(2n+2)
            else:
                a, b = c, d  # F(2n), F(2n+1)
        return a, b
    
    return fib_pair(n)[0]


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    print(fib(n))