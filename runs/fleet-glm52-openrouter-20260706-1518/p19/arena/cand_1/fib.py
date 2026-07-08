"""Fast Fibonacci via fast-doubling. fib(0)=0, fib(1)=1, exact big integers."""


def fib(n: int) -> int:
    """Return the nth Fibonacci number (fib(0)=0, fib(1)=1).

    Uses the fast-doubling identities (O(log n) big-integer operations):
        F(2k)   = F(k) * (2*F(k+1) - F(k))
        F(2k+1) = F(k+1)**2 + F(k)**2
    """
    if not isinstance(n, int):
        raise TypeError(f"fib expected int, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"fib expected non-negative n, got {n}")

    # Returns (F(k), F(k+1)) for the given k.
    def _pair(k: int) -> tuple[int, int]:
        if k == 0:
            return (0, 1)
        a, b = _pair(k >> 1)  # a = F(k//2), b = F(k//2 + 1)
        # c = F(2 * (k//2)) = F(k & ~1)
        c = a * ((b << 1) - a)
        # d = F(2 * (k//2) + 1)
        d = a * a + b * b
        if k & 1:
            return (d, c + d)
        return (c, d)

    return _pair(n)[0]


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        print(fib(int(sys.argv[1])))
    else:
        # quick sanity check
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        for i, e in enumerate(expected):
            got = fib(i)
            assert got == e, f"fib({i})={got} expected {e}"
        print("self-check ok")
