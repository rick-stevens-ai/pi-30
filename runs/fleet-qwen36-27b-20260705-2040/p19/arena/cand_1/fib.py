"""Fast Fibonacci via iterative fast-doubling — O(log n) with exact Python bigints."""


def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1).

    Uses the fast-doubling identities, applied iteratively by scanning
    the binary representation of *n* from MSB to LSB.

    Invariants at the top of each loop iteration:
        a = fib(k),  b = fib(k+1)
    where *k* is the prefix of bits consumed so far.

    Doubling step (k → 2k):
        fib(2k)   = fib(k) * (2*fib(k+1) - fib(k))
        fib(2k+1) = fib(k)^2 + fib(k+1)^2

    If the next bit is 1 we advance one more (2k → 2k+1):
        fib(2k+1) = fib(2k)   + fib(2k+1)
        fib(2k+2) = fib(2k+1) + fib(2k+1)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0

    # a = fib(k), b = fib(k+1), starting at k=0 → (0, 1)
    a, b = 0, 1

    # Walk bits from second-highest down to 0 (bit-length-1 downto 0).
    # The leading 1 is already accounted for by the initial (0,1) state.
    for bit in n.bit_length() - 1, *range(n.bit_length() - 2, -1, -1):
        # Doubling: (a, b) = (fib(2k), fib(2k+1))
        c = a * (2 * b - a)
        d = a * a + b * b
        if (n >> bit) & 1:
            # Advance one more: (fib(2k+1), fib(2k+2))
            a, b = d, c + d
        else:
            a, b = c, d

    return a
