"""Fast Fibonacci via fast-doubling. Stdlib only, exact bigint."""


def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1).

    Uses the fast-doubling identities:
        F(2k)   = F(k) * (2*F(k+1) - F(k))
        F(2k+1) = F(k+1)^2 + F(k)^2
    Runs in O(log n) bigint multiplications.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    # Iterate over bits of n from MSB to LSB, carrying (F(k), F(k+1)).
    a, b = 0, 1  # F(0), F(1)
    for bit in bin(n)[2:]:
        # Double step: (F(k), F(k+1)) -> (F(2k), F(2k+1))
        c = a * ((b << 1) - a)   # F(2k)
        d = a * a + b * b        # F(2k+1)
        a, b = c, d
        if bit == '1':
            # Advance by one: (F(2k+1), F(2k+2)) where F(2k+2)=F(2k)+F(2k+1)
            a, b = b, c + d
    return a


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print(fib(n))
