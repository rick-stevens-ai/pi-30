'''fib.py
Fast Fibonacci using fast‑doubling method (O(log n)).
Provides a single public function ``fib`` returning the nth Fibonacci number as a Python int (arbitrary‑precision).
''' 

def _fib_pair(n: int) -> tuple[int, int]:
    """Return (F(n), F(n+1)) using fast‑doubling.
    This auxiliary function is recursive but only O(log n) depth.
    """
    if n == 0:
        return (0, 1)
    else:
        a, b = _fib_pair(n >> 1)
        # a = F(k), b = F(k+1) where k = n//2
        c = a * ((b << 1) - a)   # F(2k) = F(k) * (2*F(k+1) – F(k))
        d = a * a + b * b         # F(2k+1) = F(k)^2 + F(k+1)^2
        if n & 1:
            # n is odd: return (F(2k+1), F(2k+2))
            return (d, c + d)
        else:
            # n is even: return (F(2k), F(2k+1))
            return (c, d)


def fib(n: int) -> int:
    """Return the nth Fibonacci number (0‑based).

    Args:
        n: Non‑negative integer index.
    Returns:
        The Fibonacci number F(n).
    """
    if n < 0:
        raise ValueError("n must be non‑negative")
    return _fib_pair(n)[0]


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fib.py <non‑negative integer>")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Argument must be an integer.")
        sys.exit(1)
    print(fib(n))
