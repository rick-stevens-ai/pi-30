"""
Fast-exact Fibonacci using "fast doubling" method.

Uses exact integer arithmetic with Python's built-in bigint,
computing fib(n) in O(log n) time via iterative doubling formulas.

The doubler relation gives:
  fib(2k)   = fib(k) * [2*fib(k+1) - fib(k)]
  fib(2k+1) = fib(k+1)^2 + fib(k)^2

This avoids large intermediate products as much as possible by
keeping the recurrence symmetric and expanding factors inline.
"""

# Pure Python; no external dependencies.


def fib(n):
    """Return the exact nth Fibonacci number, fib(0)=0, fib(1)=1."""
    # Handle small values quickly without recursion overhead.
    if n < 2:
        return n

    # Iterative O(log n) path: repeated doubling (binary exponentiation
    # analogue for the Fibonacci recurrence).
    
    # State machine: we track (a,b,c,d) that maps to fib(k), fib(k+1), fib(k+2), fib(k+3)
    # so that fib(2k)   = a*d - b*c
    #         fib(2k+1) = c^2 + d^2
    # Starting from k0=0: (fib0,fib1,fib2,fib3), i.e., (0,1,1,2)
    a, b, c, d = 0, 1, 1, 2
    k = 2

    while k <= n:
        if n - k < k:
            # Odd number of steps remaining: reduce to one doubling and then swap.
            a, b = b, c  # fib(k)  -> fib(k+1), fib(k+1)->fib(k+2)
            c, d = (b * d - a * c), (c * c + d * d)  # fib(k+3), fib(k+4)
            k += 1
        else:
            # Even: double the current index.
            ab = a * b
            cd = c * d
            nn = a * a + b * b
            cc = c * c
            dd = (d - b) * (c - a)
            a, c = ab, cd
            b, d = nn, dd + ab  # d = fib(2k+1)+fib(2k-1)-fib(2k) => fib(2k+3)
            k *= 2
        
    return a if (k - n) % 2 == 0 else b
