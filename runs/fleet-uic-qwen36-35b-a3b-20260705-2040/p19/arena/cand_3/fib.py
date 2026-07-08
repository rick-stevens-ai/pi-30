"""
Fast-doubling Fibonacci — O(log n) via matrix doubling identities.

F(2k)   = F(k) · [ 2·F(k+1) − F(k) ]
F(2k+1) = F(k)² + F(k+1)²

Recursive top-down; every intermediate stays an exact Python int.
"""


def fib(n: int) -> int:
    """Return the n-th Fibonacci number (0-indexed: F(0)=0, F(1)=1)."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")

    def _fib(k):
        """(F(k), F(k+1)) — fast doubling on k."""
        if k == 0:
            return (0, 1)
        fk, fm1k = _fib(k >> 1)           # (F(m), F(m+1)) where m = k//2
        t1 = fk * (2 * fm1k - fk)         # F(2m)
        t2 = fk * fk + fm1k * fm1k        # F(2m+1)
        if k & 1:                         # odd → return (F(2m+1), F(2m+2))
            return (t2, t1 + t2)
        else:                             # even → return (F(2m),   F(2m+1))
            return (t1, t2)

    return _fib(n)[0]
