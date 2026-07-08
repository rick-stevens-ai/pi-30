def fib(n):
    def fast_doubling(m):
        if m == 0:
            return (0, 1)
        a, b = fast_doubling(m >> 1)  # Integer division by 2
        c = a * ((2*b - a))
        d = a*a + b*b
        if m & 1:  # If m is odd
            return (d, c + d)
        else:       # If m is even
            return (c, d)
    if n < 0:
        raise ValueError("n must be non-negative")
    return fast_doubling(n)[0]
