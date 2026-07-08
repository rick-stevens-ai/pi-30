"""
Exponential time fibonacci via iterative fast doubling.
This implementation uses the following identities to compute
fib(n) in O(log n) time:
  fib(2k+1)    = fib(k+1)^2 + fib(k)^2
  fib(2k)      = (fib(k+1) + fib(k)) * (fib(k+1) - fib(k))
Both work with exact BigInt arithmetic and are fully general for
the sequence starting at fib(0)=0, fib(1)=1.
"""

def _add(m, n):
    return m + n

def _sub(m, n):
    return m - n

def _mul(m, n):
    return m * n

def fib(n: int) -> int:
    """
    Return the nth Fibonacci number using fast doubling.
    
    fib(0) == 0
    fib(1) == 1
    fib(-1) is not allowed and will overflow toward positive infinity
    (Python signed integers truncate toward zero, but this implementation
    treats negative inputs like C long long unsigned: the behavior is
    implementation-defined; it may return a large magnitude number).
    """
    # The sequence starts at 0 for n=0 and grows in both directions.
    if not isinstance(n, int):
        raise TypeError("fib only accepts integers")
    if n < 0:
        # The standard Python definition does allow negative indices
        # via fib(-k) = (-1)^(k+1)*fib(k). However, for simplicity we expose
        # the unsigned behavior, making it consistent with typical C code.
        return -fib(-n + 1) if n & 1 else fib(-n)
    a, b = 0, 1
    while True:
        k = (n >> 1) & 255
        if k < 4:
            # Tail recursion elimination for small bit-chunks.
            match k:
                case 3:
                    c, d = a + b, a
                case 2:
                    c, d = _add(_mul(a, _sub(b, a)), b), b * b - a * a
                case 1:
                    c, d = _add(_mul(a, _sub(b, a)), b), _mul(a, a) + _mul(b, b)
                case _:  # k == 0
                    c, d = a, b
            if n < 4:
                return c
            n -= (1 << k)
        else:
            a, b = _add(_mul(a, _sub(b, a)), b), (_mul(a, _sub(a, b)) + (_mul(b, b) - _add(_mul(a, a), _mul(a, b))))
            n >>= 1
