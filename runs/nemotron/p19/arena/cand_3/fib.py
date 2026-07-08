"""Fast Fibonacci using iterative fast-doubling (O(log n) bigint arithmetic)."""

def fib(n: int) -> int:
    """
    Return the nth Fibonacci number (fib(0)=0, fib(1)=1) using fast-doubling.

    Runs in O(log n) big-integer operations, exact Python int (arbitrary precision).
    Stdlib only, no dependencies.

    Args:
        n: non-negative integer index

    Returns:
        F(n) where F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    a, b = 0, 1  # F(0), F(1)
    for bit in bin(n)[2:]:  # iterate bits MSB to LSB
        # Double step: (F(k), F(k+1)) -> (F(2k), F(2k+1))
        c = a * ((b << 1) - a)      # F(2k) = F(k) * (2*F(k+1) - F(k))
        d = a * a + b * b           # F(2k+1) = F(k)^2 + F(k+1)^2
        if bit == '1':
            a, b = d, c + d         # advance to F(2k+1), F(2k+2)
        else:
            a, b = c, d             # advance to F(2k), F(2k+1)
    return a


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    result = fib(n)
    # Print first 20 and last 20 digits to verify
    s = str(result)
    print(f"fib({n}) has {len(s)} digits")
    if len(s) > 40:
        print(f"  first 20: {s[:20]}")
        print(f"  last 20:  {s[-20:]}")
    else:
        print(f"  value: {s}")