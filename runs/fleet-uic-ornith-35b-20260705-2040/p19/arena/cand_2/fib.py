"""
Fast-doubling Fibonacci via O(log n) big-int multiplications (Candidate #2).

Identities used:
    F(2n)     = F(n) * [2*F(n+1) - F(n)]
    F(2n + 1) = F(n)^2 + F(n+1)^2

Each step halves n → O(log n) recursive levels.
Exposure: fib(n, /) -> int
"""


def _fib(n: int):
    """Return (F(n), F(n+1)) using fast-doubling on bit decomposition."""
    if n == 0:
        return 0, 1

    a, b = _fib(n >> 1)           # a=F(k)   b=F(k+1)   k = n//2
    c = a * ((b << 1) - a)       # F(2k) = F(n)[2F(n+1)-F(n)]
    d_sq = a * a + b * b         # F(2k+1)

    return (c, d_sq) if (n & 1) == 0 else (d_sq, c + d_sq)


def fib(n: int):
    """Return the n-th Fibonacci number.

    Exact Python arbitrary-precision integer arithmetic throughout.
    fib(0)=0, fib(1)=1 follows directly from the recurrence base case.
    Time complexity: O(M(bit_size) · log n), dominated by big-int mul cost.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return _fib(n)[0]
