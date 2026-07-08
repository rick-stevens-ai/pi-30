"""
Fast Fibonacci using fast-doubling algorithm.
O(log n) time complexity, exact Python bigint arithmetic.
"""


def fib(n: int) -> int:
    """
    Return the nth Fibonacci number.
    
    Uses fast-doubling algorithm for O(log n) complexity.
    fib(0) = 0, fib(1) = 1
    
    Args:
        n: Non-negative integer index
        
    Returns:
        The nth Fibonacci number as Python int (arbitrary precision)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Iterative fast-doubling using binary representation
    # Process bits from MSB to LSB, maintaining (F(k), F(k+1))
    if n == 0:
        return 0
    
    # Find highest bit position
    bits = n.bit_length()
    f, g = 0, 1  # F(0), F(1)
    
    for i in range(bits - 1, -1, -1):
        # Double: (F(k), F(k+1)) -> (F(2k), F(2k+1)) using identities:
        # F(2k) = F(k) * (2*F(k+1) - F(k))
        # F(2k+1) = F(k)^2 + F(k+1)^2
        f2 = f * ((g << 1) - f)
        g2 = f * f + g * g
        
        if (n >> i) & 1:
            # Move to k*2 + 1: (F(2k+1), F(2k+2))
            # F(2k+2) = F(2k+1) + F(2k)
            f, g = g2, g2 + f2
        else:
            f, g = f2, g2
    
    return f


if __name__ == "__main__":
    # Quick verification
    for i in range(10):
        print(f"fib({i}) = {fib(i)}")
    
    # Test large value
    print(f"fib(200000) has {len(str(fib(200000)))} digits")