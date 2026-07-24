def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    def _fib(k: int) -> tuple[int, int]:
        # returns (F(k), F(k+1))
        if k == 0:
            return (0, 1)
        a, b = _fib(k >> 1)
        c = a * ((b << 1) - a)
        d = a * a + b * b
        if k & 1:
            return (d, c + d)
        return (c, d)
    return _fib(n)[0]

if __name__ == "__main__":
    print(fib(200000) % (10**16))  # quick sanity
