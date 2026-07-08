def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1).

    Uses fast doubling — O(log n), pure Python big ints.
    """
    if n < 2:
        return n
    def _fn(k):
        a, b = 0, 1
        bits = bin(k)[3:]          # strip '0b' and leading '1', keep remaining bits
        for bit in reversed(bits):
            c = a * (2 * b - a)
            d = a * a + b * b
            if bit == '0':
                a, b = c, d
            else:
                a, b = d, c + d
        return a

    return _fn(n)
