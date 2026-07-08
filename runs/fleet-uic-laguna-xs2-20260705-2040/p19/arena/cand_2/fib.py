"""Fast Fibonacci using fast-doubling algorithm. O(log n) time."""


def fib(n):
    """Return the nth Fibonacci number using fast-doubling.
    
    fib(0) = 0, fib(1) = 1, fib(2) = 1, fib(3) = 2, ...
    Uses Python's arbitrary precision integers (bigint).
    Time complexity: O(log n)
    """
    if n < 0:
        raise ValueError("Fibonacci not defined for negative n")
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # Iterative fast-doubling: work from LSB to MSB of n
    # Track (F(k), F(k+1)) and build up to F(n)
    result = (0, 1)  # (F(0), F(1))
    base = (0, 1)    # Will hold (F(2^i), F(2^i+1)) as we iterate
    
    bits = bin(n)[2:]  # Binary representation without '0b' prefix
    for bit in bits[1:]:  # Skip the leading 1
        # Double: from (F(k), F(k+1)) compute (F(2k), F(2k+1))
        f_k, f_k1 = base
        f_2k = f_k * (2 * f_k1 - f_k)
        f_2k1 = f_k * f_k + f_k1 * f_k1
        base = (f_2k, f_2k1)
        
        if bit == '1':
            # Add: (F(a), F(a+1)) + (F(b), F(b+1)) = (F(a+b), F(a+b+1))
            r0, r1 = result
            b0, b1 = base
            # F(a+b) = F(a)*F(b) + F(a+1)*F(b+1) - F(a)*F(b-1)
            # Simpler: use matrix multiplication identity
            # [F(a+b)  F(a+b+1)] = [F(a)  F(a+1)] * [F(b)  F(b+1)]
            #                       [F(a-1) F(a)  ]   [F(b-1) F(b)  ]
            # But we only have F(a), F(a+1). Use: F(a+b) = F(a)*F(b) + F(a+1)*F(b+1) - F(a)*F(b-1)
            # Actually simpler identity: F(m+n) = F(m)*F(n) + F(m+1)*F(n+1) - F(m)*F(n-1)
            # Even simpler: use the pair addition formula
            # (F(a+b), F(a+b+1)) where we have (F(a), F(a+1)) and (F(b), F(b+1))
            new_r0 = r0 * b0 + r1 * b1
            new_r1 = r0 * (b1 - b0) + r1 * b1
            result = (new_r0, new_r1)
    
    return result[0]


if __name__ == "__main__":
    # Quick verification
    for i, expected in enumerate([0, 1, 1, 2, 3, 5, 8, 13, 21, 34]):
        assert fib(i) == expected, f"fib({i}) = {fib(i)}, expected {expected}"
    print("Basic tests passed.")
    
    # Test n=200000
    import time
    start = time.time()
    result = fib(200000)
    elapsed = time.time() - start
    print(f"fib(200000) computed in {elapsed:.3f}s")
    print(f"fib(200000) has {result.bit_length()} bits")