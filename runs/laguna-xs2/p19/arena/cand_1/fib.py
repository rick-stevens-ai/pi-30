"""Fast Fibonacci using fast-doubling method. O(log n) time, exact Python bigint."""


def fib(n: int) -> int:
    """Return the nth Fibonacci number.

    Uses fast-doubling algorithm for O(log n) time complexity.
    fib(0) = 0, fib(1) = 1, fib(2) = 1, fib(3) = 2, ...

    Args:
        n: Non-negative integer index

    Returns:
        The nth Fibonacci number as a Python int (bigint)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return _fib_pair_iterative(n)[0]


def _fib_pair_iterative(k: int) -> tuple[int, int]:
    """Return (F(k), F(k+1)) using fast-doubling recurrence.

    Identities:
        F(2n)   = F(n) * (2*F(n+1) - F(n))
        F(2n+1) = F(n+1)^2 + F(n)^2

    Iterative version using binary expansion. O(log k) time, O(log k) space for bits.
    """
    # Build binary representation from MSB to LSB
    bits = []
    while k:
        bits.append(k & 1)
        k >>= 1
    bits.reverse()  # MSB first, skip first (always 1)

    # Start with F(0), F(1) = 0, 1
    a, b = 0, 1
    for bit in bits:
        c = a * ((b << 1) - a)       # F(2n) = F(n) * (2*F(n+1) - F(n))
        d = a * a + b * b            # F(2n+1) = F(n)^2 + F(n+1)^2
        if bit:
            a, b = d, c + d          # move to (F(2n+1), F(2n+2))
        else:
            a, b = c, d              # move to (F(2n), F(2n+1))
    return (a, b)


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print(f"F({n}) = {fib(n)}")