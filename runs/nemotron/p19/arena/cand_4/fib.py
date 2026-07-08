"""Fast Fibonacci using fast-doubling (iterative, bitwise). O(log n), stdlib only."""

def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1  # F(0), F(1)
    # Process bits from most significant to least
    for bit in bin(n)[2:]:
        # Loop invariant: a = F(k), b = F(k+1) for current prefix k
        # Fast-doubling step: compute F(2k), F(2k+1)
        c = a * (b * 2 - a)
        d = a * a + b * b
        if bit == '0':
            a, b = c, d
        else:
            a, b = d, c + d
    return a


if __name__ == "__main__":
    # Quick sanity checks
    assert [fib(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fib(200000).bit_length() == 41724  # Known value for verification
    print("All tests passed")