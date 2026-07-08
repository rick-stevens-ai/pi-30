"""Fast-doubling Fibonacci: O(log n) with exact Python integers.

Computes (F(n), F(n+1)) from (F(k), F(k+1)) where k = n//2 via the
identities:

    c  = F(2k)   = F(k)[2·F(k+1) − F(k)]      -- "sum"     index
    dd = F(2k+1) = F(k)^2 + F(k+1)^2           -- double+1

If n is even (d=0):  result is (c,   dd)          since F(n)=F(2k), F(n+1)=F(2k+1).
If n is odd  (d=1):  result is (dd, c + dd)      since F(n)=F(2k+1), F(n+1)=F(2k+2)=c+dd.

Recursion depth ≈ log₂(n), so for the standard Python recursion limit the
fast-doubling path bottoms out early and returns exact results.  For very large
n (e.g. n=200000, ~18 levels) this is completely safe.
"""


def _fib_pair(n: int):
    """Return ``(F(n), F(n+1))`` by fast doubling."""
    if n == 0:
        return 0, 1

    k = n >> 1                     # integer divide by 2
    d = n & 1                      # parity bit (bit 0 of n)

    fk, fp1 = _fib_pair(k)         # fk=F(k),   fp1=F(k+1)

    c  = fk * (2 * fp1 - fk)       # F(2k)
    dd = fk * fk + fp1 * fp1       # F(2k+1)

    if d:                          # n odd → return (F(2k+1), F(2k))
        return dd, c + dd          # the second component is F(2k+2)=F(2k)+F(2k+1)
    else:                          # n even → return (F(2k),   F(2k+1))
        return c, dd


def fib(n: int) -> int:
    """Return the ``n``-th Fibonacci number.

    * ``fib(0) == 0``
    * ``fib(1) == 1``
    * ``fib(n)`` for ``n >= 200,000`` runs in O(log n) time, well within < 1 sec.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError(f"n must be a non-negative integer, got {n!r}")
    return _fib_pair(n)[0]
