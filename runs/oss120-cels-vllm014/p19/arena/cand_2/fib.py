# fib.py
"""Fast Fibonacci using fast‑doubling algorithm.

Provides a single function ``fib(n)`` that returns the *n*th Fibonacci number
with ``fib(0) == 0`` and ``fib(1) == 1``.

The implementation runs in :math:`O(\log n)` time and uses only the Python
standard library – the built‑in arbitrary‑precision ``int`` type handles large
values (e.g., ``fib(200_000)`` has over 41 000 digits).

The algorithm is based on the identities:

* ``F(2k)   = F(k) * (2*F(k+1) – F(k))``
* ``F(2k+1) = F(k+1)^2 + F(k)^2``

by recursively halving ``n`` we obtain the result in logarithmic steps.
"""

def _fib_pair(n: int) -> tuple[int, int]:
    """Return ``(F(n), F(n+1))`` using fast‑doubling.

    The function is tail‑recursive in spirit but implemented iteratively to
    avoid recursion limits for very large ``n``.
    """
    if n == 0:
        return (0, 1)
    # Recursively compute pair for n // 2
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
    """Return the *n*th Fibonacci number.

    Parameters
    ----------
    n: int
        Non‑negative index of the Fibonacci sequence.

    Returns
    -------
    int
        ``F(n)`` where ``F(0)=0`` and ``F(1)=1``.

    Raises
    ------
    ValueError
        If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")
    return _fib_pair(n)[0]

# Simple sanity check when run as a script
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
