"""fib.py

Fast‑doubling implementation of the Fibonacci sequence.

Provides a single public function ``fib(n)`` that returns the n‑th Fibonacci
number with ``fib(0) == 0`` and ``fib(1) == 1``.

The algorithm runs in O(log n) time and uses only the Python standard library.
It works for arbitrarily large ``n`` because Python integers have unlimited
precision.
"""

def _fib_pair(n: int) -> tuple[int, int]:
    """Return ``(F(n), F(n+1))`` using the fast‑doubling recurrence.

    The recurrence relations are:
        F(2k)   = F(k) * (2*F(k+1) – F(k))
        F(2k+1) = F(k+1)**2 + F(k)**2
    This function works recursively in O(log n) depth.
    """
    if n == 0:
        return (0, 1)
    # Recursively compute pair for floor(n/2)
    a, b = _fib_pair(n >> 1)
    # Apply doubling formulas
    c = a * ((b << 1) - a)          # F(2k)
    d = a * a + b * b               # F(2k+1)
    if n & 1:
        # n is odd -> return (F(2k+1), F(2k+2))
        return (d, c + d)
    else:
        # n is even -> return (F(2k), F(2k+1))
        return (c, d)


def fib(n: int) -> int:
    """Return the n‑th Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative integer index.

    Returns
    -------
    int
        The Fibonacci number F(n).
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    return _fib_pair(n)[0]


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fib.py <n>")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("n must be an integer")
        sys.exit(1)
    print(fib(n))
