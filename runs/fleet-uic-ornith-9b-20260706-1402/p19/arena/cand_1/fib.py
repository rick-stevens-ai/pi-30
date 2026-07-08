def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1).

    Uses iterative fast-doubling for O(log n) time with exact Python bigint.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    # Process all bits of n from MSB down to bit 0
    # (a,b) always tracks (F_k, F_{k+1}) where k is built up from the prefix
    for i in range(n.bit_length() - 1, -1, -1):
        c = a * ((b << 1) - a)   # F_{2k}
        d = a * a + b * b         # F_{2k+1}
        if n & (1 << i):          # bit set → advance one more step
            a, b = d, c + d       # now (F_{2k+1}, F_{2k+2})
        else:                     # bit not set → just double
            a, b = c, d           # now (F_{2k}, F_{2k+1})
    return a
