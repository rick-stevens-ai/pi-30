"""Fast doubling Fibonacci implementation (bigint, stdlib only)."""
def fib(n):
    """Return the nth Fibonacci number, F(0)=0, F(1)=1.
    
    Uses fast‑doubling recursion: O(log n) time, works for arbitrarily large n.
    """
    if n < 0:
        raise ValueError("n must be non‑negative")
    def _fib(k):
        # returns (F(k), F(k+1))
        if k == 0:
            return 0, 1
        a, b = _fib(k >> 1)
        c = a * ((b << 1) - a)          # F(2k)   = F(k)*(2*F(k+1)-F(k))
        d = a*a + b*b                  # F(2k+1) = F(k)^2 + F(k+1)^2
        if k & 1:
            return d, c + d           # (F(2k+1), F(2k+2))
        else:
            return c, d               # (F(2k),   F(2k+1))
    return _fib(n)[0]