"""Fast Fibonacci via fast-doubling.

O(log n) arithmetic operations, exact Python bigints, stdlib only.
"""

__all__ = ["fib"]


def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1).

    Uses the fast-doubling identities:
        F(2k)   = F(k) * (2*F(k+1) - F(k))
        F(2k+1) = F(k)^2 + F(k+1)^2

    which halve the problem each step, giving O(log n) complexity.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return _fib_pair(n)[0]


def _fib_pair(n: int) -> tuple[int, int]:
    """Return (F(n), F(n+1)) via fast doubling (recursive).

    Recursion depth is O(log n); for n=200000 that is ~18 levels.
    """
    if n == 0:
        return (0, 1)
    a, b = _fib_pair(n >> 1)          # (F(k), F(k+1))  with k = n // 2
    c = a * ((b << 1) - a)            # F(2k)   = F(k) * (2*F(k+1) - F(k))
    d = a * a + b * b                 # F(2k+1) = F(k)^2 + F(k+1)^2
    if n & 1:
        return (d, c + d)             # (F(2k+1), F(2k+2))
    return (c, d)                     # (F(2k),   F(2k+1))


if __name__ == "__main__":
    import sys

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    result = fib(n)
    if n > 50:
        print(f"fib({n}) has {len(str(result))} digits")
    else:
        print(result)