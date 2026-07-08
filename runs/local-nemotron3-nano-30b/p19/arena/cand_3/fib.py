def fib(n):
    \"\"\"\n    Return the nth Fibonacci number using the fast-doubling algorithm.\n    Runs in O(log n) time and uses Python's native arbitrary-precision ints.\n    >>> [fib(i) for i in range(10)]\n    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]\n    >>> fib(0)\n    0\n    >>> fib(1)\n    1\n    \"\"\"\n    def _fib_pair(k):
        if k == 0:
            return (0, 1)
        else:
            a, b = _fib_pair(k >> 1)
            c = a * ((b << 1) - a)   # F(2m) = F(m)*(2*F(m+1) – F(m))
            d = a*a + b*b           # F(2m+1) = F(m)^2 + F(m+1)^2
            if k & 1:
                return (d, c + d)
            else:
                return (c, d)
    return _fib_pair(n)[0]\n\n\nif __name__ == \"__main__\":\n    # Simple sanity check when run as a script.\n    import sys\n    if len(sys.argv) > 1:\n        n = int(sys.argv[1])\n        print(f\"Fib({n}) = {fib(n)}\")\n