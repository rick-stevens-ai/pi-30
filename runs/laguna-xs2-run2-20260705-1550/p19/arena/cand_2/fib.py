"""
Fast Fibonacci using fast-doubling algorithm.
O(log n) time complexity, exact Python bigint arithmetic.
"""

def fib(n):
    """
    Return the nth Fibonacci number using fast-doubling.
    fib(0) = 0, fib(1) = 1, fib(2) = 1, fib(3) = 2, ...
    
    Uses the identities:
        F(2k) = F(k) * (2*F(k+1) - F(k))
        F(2k+1) = F(k+1)² + F(k)²
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    
    # Iterative fast-doubling: process all bits from MSB to LSB
    # Start with (F(0), F(1)) = (0, 1)
    a, b = 0, 1  # F(k), F(k+1) where k starts at 0
    bits = bin(n)[2:]  # All bits including leading 1
    
    for bit in bits:
        # Compute F(2k) and F(2k+1) from F(k) and F(k+1)
        c = a * (2 * b - a)  # F(2k)
        d = a * a + b * b    # F(2k+1)
        
        if bit == '1':
            # Current bit is 1: advance from (F(2k), F(2k+1)) to (F(2k+1), F(2k+2))
            a, b = d, c + d
        else:
            # Current bit is 0: stay at (F(2k), F(2k+1))
            a, b = c, d
    
    return a


if __name__ == "__main__":
    # Quick test
    print(fib(0))   # 0
    print(fib(1))   # 1
    print(fib(10))  # 55
    print(fib(50))  # 12586269025