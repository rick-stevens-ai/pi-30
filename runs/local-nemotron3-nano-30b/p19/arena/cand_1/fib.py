"""Return the nth Fibonacci number using fast-doubling O(log n)."""

def fib(n: int) -> int:
    """
    Return the nth Fibonacci number (0‑indexed) using the fast‑doubling method.
    Runs in O(log n) time and uses Python's native arbitrary‑precision integers.

    Parameters
    ----------
    n : int
        Non‑negative index of the desired Fibonacci number.

    Returns
    -------
    int
        The nth Fibonacci number, where fib(0)=0, fib(1)=1.

    Raises
    ------
    ValueError
        If n is negative.
    """
    if n < 0:
        raise ValueError("n must be a non‑negative integer")

    # fast-doubling helper that returns (F(k), F(k+1))
    def _fib_pair(k: int):
        if k == 0:
            return (0, 1)
        # Recursively compute pair for floor(k/2)
        a, b = _fib_pair(k >> 1)

        # Apply the doubling formulas
        c = a * ((b << 1) - a)   # F(2k)
        d = a * a + b * b        # F(2k+1)

        if k & 1:                # If k is odd
            return (d, c + d)    # (F(2k+1), F(2k+2))
        else:                    # If k is even
            return (c, d)        # (F(2k), F(2k+1))

    # The first element of the pair is F(n)
    return _fib_pair(n)[0]