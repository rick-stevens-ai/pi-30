"""
Fibonacci via fast-doubling (iterative, O(log n)).

Uses the identities:
    F(2k)   = F(k) * (2*F(k+1) - F(k))
    F(2k+1) = F(k)^2 + F(k+1)^2

Walks the bits of n from MSB to LSB so no recursion is needed —
safe for arbitrarily large n without hitting Python's recursion limit.
"""


def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1)."""
    if n < 0:
        raise ValueError("n must be non-negative")

    # (a, b) represents (F(k), F(k+1)), starting at k=0
    a, b = 0, 1

    # Shift right to find the most-significant bit.
    # We process bits from MSB down to bit 0 (skipping the leading 1).
    mask = 1 << n.bit_length()  # one past the MSB

    while mask > 1:
        # Doubling step: from (F(k), F(k+1)) produce (F(2k), F(2k+1))
        c = a * (2 * b - a)       # F(2k)
        d = a * a + b * b         # F(2k+1)
        a, b = c, d

        if n & mask:
            # Advance one more: (F(2k+1), F(2k+2))
            a, b = b, c + d

        mask >>= 1

    return a
