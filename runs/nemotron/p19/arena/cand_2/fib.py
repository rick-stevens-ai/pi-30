"""Fast Fibonacci using iterative fast-doubling (bitwise, bottom-up)."""


def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1) in O(log n) time.

    Uses iterative fast-doubling with bitwise decomposition of n.
    Avoids recursion overhead; processes bits from MSB to LSB.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    # F(k) = a, F(k+1) = b  initially for k = 0
    a, b = 0, 1

    # Iterate over bits of n from most significant to least
    for bit in reversed(bin(n)[2:]):
        # Fast-doubling step: from F(k), F(k+1) compute F(2k), F(2k+1)
        # c = F(2k) = F(k) * (2*F(k+1) - F(k))
        # d = F(2k+1) = F(k)^2 + F(k+1)^2
        c = a * ((b << 1) - a)
        d = a * a + b * b

        if bit == '0':
            # k -> 2k
            a, b = c, d
        else:
            # k -> 2k+1
            a, b = d, c + d

    return a


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        print(fib(n))
    else:
        # Quick sanity checks
        assert fib(0) == 0
        assert fib(1) == 1
        assert fib(2) == 1
        assert fib(3) == 2
        assert fib(10) == 55
        assert fib(20) == 6765
        print("All tests passed")