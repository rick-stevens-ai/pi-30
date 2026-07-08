def fib(n):
    \"\"\"Return the nth Fibonacci number using fast‑doubling (O(log n)) arithmetic with Python's built-in bigint.

    The implementation uses the fast‑doubling recurrence:
        F(2k)   = F(k) * (2*F(k+1) – F(k))
        F(2k+1) = F(k)^2 + F(k+1)^2
    It runs in O(log n) time and works with arbitrarily large integers because it
    relies only on Python's native unlimited‑precision ints.
    \"\"\"
    if n < 0:
        raise ValueError(\"n must be a non‑negative integer\")

    def _pair(k):
        # returns (F(k), F(k+1))
        if k == 0:
            return (0, 1)
        else:
            a, b = _pair(k >> 1)               # (F(m), F(m+1)) with m = k//2
            c = a * ((b << 1) - a)             # F(2m)
            d = a*a + b*b                      # F(2m+1)
            if k & 1:                          # k is odd
                return (d, c + d)
            else:
                return (c, d)

    return _pair(n)[0]

# Simple self‑test when run as a script
if __name__ == \"__main__\":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    print(f\"Fibonacci({n}) = {fib(n)}\")