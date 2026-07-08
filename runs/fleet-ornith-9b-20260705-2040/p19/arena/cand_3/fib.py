"""Fast Fibonacci via fast-doubling identities.

F(2k)   = F(k) * (2*F(k+1) - F(k))
F(2k+1) = F(k)^2 + F(k+1)^2

Recurrence: O(log n) multiplications, no recursion limit issues.
"""


def fib(n):
    """Return the nth Fibonacci number with exact Python bigint arithmetic.

    Parameters
    ----------
    n : int or int-like
        Index (non-negative).  fib(0)=0, fib(1)=1.

    Returns
    -------
    int
        Exact integer value of fib(n).
    """
    # Start from the highest set bit and walk down.
    # At each step we have F(k), F(k+1) for k = current position.
    bits = bin(n)[3:]              # strip "0b" and leading '0' (zero-width)
    a, b = 0, 1                    # F(0)=a, F(1)=b
    for bit in reversed(bits):     # MSB → LSB
        c = a * ((2 * b) - a)     # F(2k)
        a = a * a + b * b         # F(2k+1)
        if bit == "1":
            a, b = b, a + b       # advance one step (F(k),F(k+1)) -> F(k+1),F(k+2))
    return a
