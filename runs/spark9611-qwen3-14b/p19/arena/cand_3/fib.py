def fib(n):
    def fast_doubling(n):
        if n == 0:
            return (0, 1)
        a, b = fast_doubling(n >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        if n & 1:
            return (d, c + d)
        else:
            return (c, d)
    return fast_doubling(n)[0]