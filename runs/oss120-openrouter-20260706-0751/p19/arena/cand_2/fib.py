def fib(n: int) -> int:
    """Return the nth Fibonacci number using fast doubling (O(log n)).

    Args:
        n: Non‑negative integer where fib(0)=0, fib(1)=1.
    Returns:
        The nth Fibonacci number as a Python ``int`` (arbitrary‑precision).
    """
    if n < 0:
        raise ValueError("n must be non‑negative")

    def _fib_pair(k: int) -> tuple[int, int]:
        """Return (F(k), F(k+1)) using the fast‑doubling recurrence.
        """
        if k == 0:
            return (0, 1)
        # Recursively compute half
        a, b = _fib_pair(k >> 1)
        # Apply doubling formulas
        c = a * ((b << 1) - a)  # F(2k) = F(k) * (2*F(k+1) – F(k))
        d = a * a + b * b       # F(2k+1) = F(k)^2 + F(k+1)^2
        if k & 1:
            return (d, c + d)   # (F(2k+1), F(2k+2))
        else:
            return (c, d)       # (F(2k), F(2k+1))

    return _fib_pair(n)[0]
