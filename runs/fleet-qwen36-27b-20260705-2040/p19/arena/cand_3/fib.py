"""Fibonacci via iterative fast-doubling (O(log n), exact bigint).

Uses the identities:
    F(2k)   = F(k) * (2*F(k+1) - F(k))
    F(2k+1) = F(k+1)**2 + F(k)**2

Walks the bits of n from MSB to LSB (left-to-right doubling),
maintaining the pair (F(k), F(k+1)) without recursion."""

def fib(n: int) -> int:
    """Return the nth Fibonacci number. fib(0)=0, fib(1)=1."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0

    # Start with k=1: pair (F(1), F(2)) = (1, 1)
    a, b = 1, 1  # a = F(k), b = F(k+1)

    # Process remaining bits of n from the second-highest bit down to bit 0.
    # The MSB is always 1 (we initialized k=1), so skip it.
    bits = n.bit_length() - 1  # number of bits to process after MSB
    for _ in range(bits):
        # Double step: go from k -> 2k
        c = a * (2 * b - a)   # F(2k)
        d = a * a + b * b      # F(2k+1)
        a, b = c, d

        # If the next bit is 1, advance one more: 2k -> 2k+1
        if (n >> (bits - 1 - _)) & 1:
            a, b = b, c + d

    return a
