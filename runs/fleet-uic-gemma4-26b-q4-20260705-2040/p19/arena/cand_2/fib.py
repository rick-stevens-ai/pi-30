import sys

# Increase integer string conversion limit for large numbers to allow printing/stringifying if needed
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)

def fib(n):
    """
    Compute the nth Fibonacci number using the fast doubling method.
    Complexity: O(log n) multiplications of large integers.
    
    Fibonacci sequence definition:
    F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)

    Fast doubling formulas used:
    F(2k)   = F(k) * [2*F(k+1) - F(k)]
    F(2k+1) = F(k+1)^2 + F(k)^2
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    
    # a is F_k, b is F_{k+1}
    a, b = 0, 1
    
    # Process bits of n from MSB to LSB (skipping '0b' prefix)
    for bit in bin(n)[2:]:
        # Stage 1: Double the current index k -> 2k
        # c = F_{2k}, d = F_{2k+1}
        c = a * ((b << 1) - a)
        d = a * a + b * b
        
        a, b = c, d
        
        if bit == '1':
            # Stage 2: Move from 2k -> 2k+1
            # (F_{2k}, F_{2k+1}) -> (F_{2k+1}, F_{2k+2})
            a, b = b, a + b
            
    return a

if __name__ == "__main__":
    import time

    # Validation tests
    test_cases = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 5, 6: 8, 7: 13, 10: 55}
    for n, expected in test_cases.items():
        actual = fib(n)
        assert actual == expected, f"Error at F({n}): expected {expected}, got {actual}"
    print("Basic tests passed.")

    # Performance benchmark: n = 200,000
    target = 200000
    start = time.time()
    res = fib(target)
    end = time.time()
    
    duration = end - start
    print(f"F({target}) computed in {duration:.4f} seconds.")
    
    # Output verification info without overwhelming terminal
    s_res = str(res)
    print(f"Number of digits: {len(s_res)}")
    print(f"First 10 digits: {s_res[:10]}")
    print(f"Last 10 digits:  {s_res[-10:]}")
