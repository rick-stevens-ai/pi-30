"""Fast Fibonacci using fast-doubling method. O(log n) for exact bigint."""


def fib(n: int) -> int:
    """Return the nth Fibonacci number.
    
    Uses fast-doubling algorithm for O(log n) complexity.
    fib(0) = 0, fib(1) = 1, fib(2) = 1, fib(3) = 2, ...
    Exact Python bigint arithmetic.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # Iterative fast-doubling using binary representation
    # Process bits from MSB to LSB, maintaining (fib(k), fib(k+1))
    # Start with k=1, result = (fib(1), fib(2)) = (1, 1)
    result = (1, 1)  # (fib(1), fib(2))
    bits = bin(n)[3:]  # Binary of n, skip '0b1'
    
    for bit in bits:
        a, b = result
        # Double: compute (fib(2k), fib(2k+1)) from (fib(k), fib(k+1))
        c = a * ((b << 1) - a)      # fib(2k)
        d = a * a + b * b           # fib(2k+1)
        if bit == '0':
            result = (c, d)         # k -> 2k
        else:
            result = (d, c + d)     # k -> 2k+1
    
    return result[0]


if __name__ == "__main__":
    # Quick verification
    for i in range(10):
        print(f"fib({i}) = {fib(i)}")
    
    # Test large value
    import sys
    sys.set_int_max_str_digits(0)  # Allow arbitrary string conversion
    result = fib(200000)
    print(f"fib(200000) has {len(str(result))} digits")