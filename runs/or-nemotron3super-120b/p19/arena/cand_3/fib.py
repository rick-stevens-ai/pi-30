def fib(n: int) -> int:
    """
    Return the nth Fibonacci number using the fast doubling method.
    fib(0) = 0, fib(1) = 1.
    Runs in O(log n) time and O(log n) space due to recursion depth.
    Uses Python's arbitrary precision integers.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    def _fib(k: int) -> tuple[int, int]:
        """Return (F(k), F(k+1))"""
        if k == 0:
            return (0, 1)
        else:
            a, b = _fib(k >> 1)
            c = a * ((b << 1) - a)          # F(2m)   = F(m) * [2*F(m+1) − F(m)]
            d = a * a + b * b               # F(2m+1) = F(m)^2 + F(m+1)^2
            if k & 1:
                return (d, c + d)           # (F(2m+1), F(2m+2))
            else:
                return (c, d)               # (F(2m), F(2m+1))
    return _fib(n)[0]


if __name__ == "__main__":
    # Simple self-test
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(10) == 55
    assert fib(20) == 6765
    # Test large n (200000) - just ensure it runs without error and produces an integer
    # The value is huge; we can check its length or a known property.
    # For sanity, compute fib(200000) modulo something and compare with known?
    # We'll just ensure it returns an integer and the number of bits is reasonable.
    val = fib(200000)
    assert isinstance(val, int)
    # Number of digits in base 10 approx n*log10(phi) - log10(sqrt(5))
    # For n=200000, digits ~ 200000*0.208987... ≈ 41797
    # So we expect around 41797 digits.
    # We'll check that it's positive and has many digits.
    assert val > 0
    # Optional: compute bit length
    # bit length approx n*log2(phi) ≈ 200000*0.69424... = 138848 bits
    # So bit length should be around 138848.
    bl = val.bit_length()
    assert bl > 138000 and bl < 140000, f"Unexpected bit length: {bl}"
    print("All tests passed.")