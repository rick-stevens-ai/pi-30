def _fib_pair(n):
    if n == 0:
        return (0, 1)
    else:
        a, b = _fib_pair(n >> 1)
        c = a * ((b << 1) - a)
        d = a * a + b * b
        if n & 1:
            return (d, c + d)
        else:
            return (c, d)

def fib(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    return _fib_pair(n)[0]